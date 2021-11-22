from scrapy_djangoitem import DjangoItem

from loxone.apps.measurements.models import Measurement


class MeasurementItem(DjangoItem):
    django_model = Measurement
