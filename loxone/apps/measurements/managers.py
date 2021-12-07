import operator
from datetime import datetime, date, timedelta
from functools import reduce
from statistics import mean

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Avg, F, Max, Q, Min, Func, FloatField
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
            ).exclude(
                type="unknown"
            ).annotate(
                day=TruncDay("time"),
                zone_name=F("zone"),
                type_name=F("type"),
            ).values(
                "building",
                "day",
                "zone_name",
                "type_name"
            ).annotate(
                average_value=Round(Avg("value", output_field=FloatField())),
                min_value=Min("value", output_field=FloatField()),
                max_value=Max("value", output_field=FloatField()),
            ).values(
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
            while day < today:
                days[day.strftime("%d.%m.%Y")] = {}
                for zone in building["zones"]:
                    days[day.strftime("%d.%m.%Y")][zone] = ["-"] * (
                            len(building["types"]) * 3
                    )
                day += timedelta(days=1)
            days["summary_statistics"] = {}
            for zone in building["zones"]:
                days["summary_statistics"][zone] = []
                for type_number in range(len(building["types"]) * 3):
                    if type_number % 3 == 0:
                        days["summary_statistics"][zone].append([])
                    if type_number % 3 == 1:
                        days["summary_statistics"][zone].append(None)
                    if type_number % 3 == 2:
                        days["summary_statistics"][zone].append(None)

        return templates_data

    def get_templates_data(self):
        type_labels = ["temperature", "humidity", "CO2"]
        templates_data = self.get_empty_templates_data()
        final_summary_statistics = {}
        for measurement in self.month_statistics():
            try:
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
                    summary_statistics = templates_data[measurement["building__name"]]["days"][
                        "summary_statistics"
                    ][measurement["zone_name"]]
                    final_summary_statistics_key = f'{measurement["building__name"]}{measurement["zone_name"]}'
                    if final_summary_statistics_key not in final_summary_statistics:
                        final_summary_statistics[
                            final_summary_statistics_key
                        ] = summary_statistics
                    summary_statistics_key = key + 3 * type_labels.index(measurement["type_name"])
                    summary_statistics_value = summary_statistics[summary_statistics_key]
                    if value_name == "max_value":
                        if not summary_statistics_value or summary_statistics_value < measurement[
                            value_name
                        ]:
                            summary_statistics[summary_statistics_key] = measurement[
                                value_name
                            ]
                    if value_name == "min_value":
                        if not summary_statistics_value or summary_statistics_value > measurement[
                            value_name
                        ]:
                            summary_statistics[summary_statistics_key] = measurement[
                                value_name
                            ]
                    if value_name == "average_value":
                        summary_statistics_value.append(
                            measurement[
                                value_name
                            ]
                        )
            except Exception as e:
                print(e)
        for key1, statistics in final_summary_statistics.items():
            statistics_to_change = statistics
            for key2, statistic in enumerate(statistics):
                if key2 % 3 == 0:
                    if statistic:
                        statistics_to_change[key2] = round(mean(statistic), 2)
                    else:
                        statistics_to_change[key2] = "-"
                else:
                    if not statistic:
                        statistics_to_change[key2] = "-"

        return templates_data
