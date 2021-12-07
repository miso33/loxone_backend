from datetime import datetime, timedelta
from statistics import mean

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .factories import BuildingFactory
from .factories import MeasurementFactory
from .models import Measurement, Building

User = get_user_model()


class MeasurementAPITestCase(APITestCase):
    def test_month_average_statistics_by_day(self):
        building_number = 3
        types = ["temperature", "humidity", "CO2"]
        zone_number = 5
        days = 5
        measurements = {}
        buildings = BuildingFactory.create_batch(building_number)
        for building in buildings:
            for type in types:
                for zone_number in range(1, zone_number + 1):
                    MeasurementFactory.reset_sequence(0)
                    for day in range(1, days + 1):
                        average = []
                        today_midnight = datetime.combine(
                            datetime.today(), datetime.min.time()
                        ) - timedelta(days=day)
                        today_midnight_string = today_midnight.strftime("%d.%m.%Y")
                        key = f"{building.name}*{type}*Zone{zone_number}*{today_midnight_string}"
                        measurements[key] = MeasurementFactory.create_batch(
                            24,
                            building=building,
                            type=type,
                            zone=f"Zone{zone_number}",
                            url=f"Zone{zone_number}",
                        )
                        for measurement in measurements[key]:
                            average.append(measurement.value)
                        measurements[key] = round(mean(average), 2)
        measurement_statistics = Measurement.objects.month_statistics()
        for stat in measurement_statistics:
            day_key = stat["day"].strftime("%d.%m.%Y")
            stat_key = f"{stat['building__name']}*{stat['type_name']}*{stat['zone_name']}*{day_key}"
            self.assertIn(stat_key, measurements)
            self.assertAlmostEqual(
                measurements[stat_key], float(stat["average_value"]), 1
            )

    def test_month_max_statistics_by_day(self):
        building_number = 3
        types = ["temperature", "humidity", "CO2"]
        zone_number = 5
        days = 5
        measurements = {}
        buildings = BuildingFactory.create_batch(building_number)
        for building in buildings:
            for type in types:
                for zone_number in range(1, zone_number + 1):
                    MeasurementFactory.reset_sequence(0)
                    for day in range(1, days + 1):
                        average = []
                        today_midnight = datetime.combine(
                            datetime.today(), datetime.min.time()
                        ) - timedelta(days=day)
                        today_midnight_string = today_midnight.strftime("%d.%m.%Y")
                        key = f"{building.name}*{type}*Zone{zone_number}*{today_midnight_string}"

                        measurements[key] = MeasurementFactory.create_batch(
                            24,
                            building=building,
                            type=type,
                            zone=f"Zone{zone_number}",
                            url=f"Zone{zone_number}",
                        )
                        for measurement in measurements[key]:
                            average.append(measurement.value)
                        measurements[key] = max(average)
        measurement_statistics = Measurement.objects.month_statistics()

        for stat in measurement_statistics:
            day_key = stat["day"].strftime("%d.%m.%Y")
            stat_key = f"{stat['building__name']}*{stat['type_name']}*{stat['zone_name']}*{day_key}"
            self.assertIn(stat_key, measurements)
            self.assertAlmostEqual(measurements[stat_key], float(stat["max_value"]), 1)

    def test_month_min_statistics_by_day(self):
        building_number = 3
        types = ["temperature", "humidity", "CO2"]
        zone_number = 5
        days = 5
        measurements = {}
        buildings = BuildingFactory.create_batch(building_number)
        for building in buildings:
            for type in types:
                for zone_number in range(1, zone_number + 1):
                    MeasurementFactory.reset_sequence(0)
                    for day in range(1, days + 1):
                        average = []
                        today_midnight = datetime.combine(
                            datetime.today(), datetime.min.time()
                        ) - timedelta(days=day)
                        today_midnight_string = today_midnight.strftime("%d.%m.%Y")
                        key = f"{building.name}*{type}*Zone{zone_number}*{today_midnight_string}"
                        measurements[key] = MeasurementFactory.create_batch(
                            24,
                            building=building,
                            type=type,
                            zone=f"Zone{zone_number}",
                            url=f"Zone{zone_number}",
                        )
                        for measurement in measurements[key]:
                            average.append(measurement.value)
                        measurements[key] = min(average)
        measurement_statistics = Measurement.objects.month_statistics()

        for stat in measurement_statistics:
            day_key = stat["day"].strftime("%d.%m.%Y")
            stat_key = f"{stat['building__name']}*{stat['type_name']}*{stat['zone_name']}*{day_key}"
            self.assertIn(stat_key, measurements)
            self.assertAlmostEqual(measurements[stat_key], float(stat["min_value"]), 1)

    def test_zone_type_list(self):
        types_combinations = [
            ["temperature", "humidity", "CO2"],
            ["temperature", "humidity"],
            ["temperature", "CO2"],
        ]
        measurements_combinations = {}
        for building_key, building in enumerate(
                BuildingFactory.create_batch(len(types_combinations))
        ):
            zones = []
            for type_key, type_name in enumerate(types_combinations[building_key]):
                zones.append(f"Zone{building_key + type_key}")
                MeasurementFactory.create_batch(
                    10,
                    building=building,
                    type=type_name,
                    zone=f"Zone{building_key + type_key}",
                )

            measurements_combinations[building.id] = {
                "building_name": building.name,
                "types": types_combinations[building_key],
                "zones": zones,
            }
        for measurement in Measurement.objects.zone_type_list():
            measurements_combination = measurements_combinations[
                measurement["building__id"]
            ]
            self.assertEqual(
                measurements_combination["building_name"], measurement["building__name"]
            )
            self.assertListEqual(
                measurements_combination["zones"], measurement["zones"]
            )
            self.assertListEqual(
                measurements_combination["types"], measurement["types"]
            )

    def test_last_measurements(self):
        types_combination = ["temperature", "humidity", "CO2"]
        zones_combination = [f"Zone{number}" for number in range(0, 3)]
        last_measurements = []
        for zone in zones_combination:
            for type_name in types_combination:
                last_measurements.append(
                    MeasurementFactory.create(zone=zone, type=type_name)
                )

        for zone in zones_combination:
            for type_name in types_combination:
                MeasurementFactory.create_batch(10, zone=zone, type=type_name)
        measurements = Measurement.objects.last_measurements()
        for last_measurement in last_measurements:
            self.assertEqual(
                measurements[
                    f"{last_measurement.zone} {last_measurement.type}"
                ],
                last_measurement.value,
            )

    def test_get_empty_templates_data(self):
        today = datetime.today()
        buildings = BuildingFactory.create_batch(1)
        types = ["temperature", "humidity", "CO2"]
        zone_number = 2
        for building in buildings:
            for type_name in types:
                for zone_number in range(1, zone_number + 1):
                    day = today.replace(day=1)
                    while day < today:
                        MeasurementFactory.create_batch(
                            24,
                            building=building,
                            type=type_name,
                            zone=f"Zone{zone_number}",
                            url=f"Zone{zone_number}",
                        )
                        day += timedelta(days=1)
                    MeasurementFactory.reset_sequence(0)
        empty_templates = Measurement.objects.get_empty_templates_data()
        print(empty_templates)
        # for building, empty_template in empty_templates.items():
        #     self.assertTrue(Building.objects.filter(name=building).exists())
        #     self.assertEqual(len(empty_template['days']), today.day)
        #     for day in empty_template['days'].values():
        #         for zone, value in day.items():
        #             self.assertTrue(Measurement.objects.filter(zone=zone).exists())
        #             self.assertEqual(len(value), len(types) * 3)

    def test_get_templates_data(self):
        today = datetime.today()
        buildings = BuildingFactory.create_batch(1)
        types = ["temperature", "humidity", "CO2"]
        zone_number = 2
        for building in buildings:
            for type_name in types:
                for zone_number in range(1, zone_number + 1):
                    day = today.replace(day=1)
                    while day < today:
                        MeasurementFactory.create_batch(
                            24,
                            building=building,
                            type=type_name,
                            zone=f"Zone{zone_number}",
                            url=f"Zone{zone_number}",
                        )
                        day += timedelta(days=1)
                    MeasurementFactory.reset_sequence(0)

        templates = Measurement.objects.get_templates_data()
        # print(templates)
        print(templates)
        # for building, empty_template in empty_templates.items():
        #     self.assertTrue(Building.objects.filter(name=building).exists())
        #     self.assertEqual(len(empty_template['days']), today.day)
        #     for day in empty_template['days'].values():
        #         for zone, value in day.items():
        #
        #             self.assertEqual(len(value), len(types) * 3)
    #
    # def test_month_average_statistics_by_month(self):
    #     building_number = 3
    #     types = ["temperature", "humidity", "CO2"]
    #     zone_number = 3
    #     days = 3
    #     measurements = {}
    #     buildings = BuildingFactory.create_batch(building_number)
    #     for building in buildings:
    #         for type in types:
    #             for zone_number in range(1, zone_number + 1):
    #                 average = []
    #                 MeasurementFactory.reset_sequence(0)
    #                 key = f"{building.name}*{type}*Zone{zone_number}"
    #                 measurements[key] = []
    #                 for day in range(1, days + 1):
    #                     measurements[key] += MeasurementFactory.create_batch(
    #                         24,
    #                         building=building,
    #                         type=type,
    #                         zone="Zone{}".format(zone_number),
    #                         url="Zone{}".format(zone_number),
    #                     )
    #                 for measurement in measurements[key]:
    #                     average.append(measurement.value)
    #                 measurements[key] = round(mean(average), 2)
    #     print(measurements)
    #     print(len(measurements))
    #                 # print(measurements[key])
    #     measurement_statistics = Measurement.objects.month_statistics()
    # for stat in measurement_statistics:
    #     day_key = stat["day"].strftime("%d.%m.%Y")
    #     stat_key = "{0}*{1}*{2}*{3}".format(
    #         stat["building__name"], stat["type_name"], stat["zone_name"], day_key
    #     )
    #     self.assertIn(stat_key, measurements)
    #     self.assertAlmostEqual(
    #         measurements[stat_key], float(stat["average_value"]), 1
    #     )
