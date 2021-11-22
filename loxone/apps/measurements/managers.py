import operator
from datetime import datetime, date, timedelta
from functools import reduce

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Avg, F, Max, Q, Min, Func
from django.db.models.functions import TruncDay


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s, 2)"


class MeasurementQuerySet(models.QuerySet):
    def month_statistics(self):
        yesterday = date.today() - timedelta(days=1)
        return (
            self.filter(
                time__year=yesterday.year,
                time__month=yesterday.month,
                building__status="active",
            )
            .exclude(type="unknown")
            .annotate(
                day=TruncDay("time"),
                zone_name=F("zone"),
                type_name=F("type"),
            )
            .values("building", "day", "zone_name", "type_name")
            .annotate(
                average_value=Round(Avg("value")),
                min_value=Min("value"),
                max_value=Max("value"),
            )
            .values(
                "building__name",
                "day",
                "zone_name",
                "type_name",
                "average_value",
                "max_value",
                "min_value",
            )
            .order_by("building__name", "day", "zone_name", "-type_name")
        )

    def last_measurements(self):
        combinations = (
            self.values("zone", "type")
            .annotate(time=Max("time"))
            .order_by("zone", "type")
        )
        if combinations:
            q_object = reduce(operator.or_, (Q(**x) for x in combinations))
            return self.filter(q_object).values("zone", "type", "value")
        return {}

    def zone_type_list(self):
        return (
            self.filter(building__status="active")
            .exclude(type="unknown")
            .values("building__id", "building__name")
            .order_by(
                "building__name",
            )
            .annotate(
                zones=ArrayAgg("zone", distinct=True, ordering="zone"),
                types=ArrayAgg("type", distinct=True, ordering="-type"),
            )
        )


class MeasurementManager(models.Manager):
    def get_queryset(self):
        return MeasurementQuerySet(self.model, using=self._db).filter(is_removed=False)

    def month_statistics(self):
        return self.get_queryset().month_statistics()

    def last_measurements(self):
        last_measurements = {}
        for measurement in self.get_queryset().last_measurements():
            last_measurements[
                "{} {}".format(measurement["zone"], measurement["type"])
            ] = float(measurement["value"])
        return last_measurements

    def zone_type_list(self):
        return self.get_queryset().zone_type_list()

    def get_empty_templates_data(self):
        templates_data = {}
        today = datetime.today()
        for building in self.zone_type_list():
            building_template = templates_data[building["building__name"]] = {}
            building_template["zone_list"] = building["zones"]
            building_template["type_list"] = building["types"]
            building_template["days"] = {}
            days = building_template["days"]
            day = today.replace(day=1)
            while day <= today:
                days[day.strftime("%d.%m.%Y")] = {}
                for zone in building["zones"]:
                    days[day.strftime("%d.%m.%Y")][zone] = ["-"] * (
                        len(building["types"]) * 3
                    )
                day += timedelta(days=1)
        return templates_data

    def get_templates_data(self):
        type_labels = ["temperature", "humidity", "CO2"]
        templates_data = self.get_empty_templates_data()
        for measurement in self.month_statistics():
            for key, value_name in enumerate(
                ["average_value", "min_value", "max_value"]
            ):
                templates_data[measurement["building__name"]]["days"][
                    measurement["day"].strftime("%d.%m.%Y")
                ][measurement["zone_name"]][
                    key + 3 * type_labels.index(measurement["type_name"])
                ] = measurement[
                    value_name
                ]
        return templates_data
