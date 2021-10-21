# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from loxone.apps.buildings.models import Building
from loxone.apps.measurements.models import Measurement


class MeasurementPipeline:
    def __init__(self, *args, **kwargs):
        self.items = []

    def close_spider(self, spider):
        to_save = []
        for item in self.items:
            measurement = Measurement()
            measurement.value = item["value"]
            measurement.time = item["time"]
            measurement.type = item["type"]
            measurement.zone = item["zone"]
            measurement.building = Building.objects.get(pk=item["building"])
            measurement.url = item["url"]
            to_save.append(measurement)
        Measurement.objects.bulk_create(to_save)

    def process_item(self, item, spider):
        self.items.append(item)
