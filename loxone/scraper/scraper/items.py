from scrapy_djangoitem import DjangoItem

from loxone.apps.measurements.models import Measurement


class MeasurementItem(DjangoItem):
    django_model = Measurement

# for item in self.items:
#     measurement_item = MeasurementItem()
#     # measurement_item["pk"] = pk
#     measurement_item["value"] = item["value"]
#     measurement_item["time"] = item["time"]
#     measurement_item["type"] = item["type"]
#     measurement_item["zone"] = item["zone"]
#     measurement_item["building"] = Building.objects.get(pk=item["building"])
#     measurement_item["url"] = item["url"]
#     measurement_item.save()
# # MeasurementItem.objects.bulk_create(to_save)
