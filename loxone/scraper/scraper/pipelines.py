from loxone.apps.measurements.models import Measurement
from sentry_sdk import capture_exception


class MeasurementPipeline:
    def __init__(self, *args, **kwargs):
        self.items = []

    def close_spider(self, spider):
        try:
            to_save = []
            for item in self.items:
                measurement = Measurement()
                measurement.value = item["value"]
                measurement.time = item["time"]
                measurement.type = item["type"]
                measurement.zone = item["zone"]
                measurement.building_id = item["building"]
                measurement.url = item["url"]
                to_save.append(measurement)
            Measurement.objects.bulk_create(to_save, ignore_conflicts=True)
        except Exception as e:
            print(e)
            capture_exception(e)

    def process_item(self, item, spider):
        self.items.append(item)
