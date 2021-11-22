from datetime import datetime, timedelta

import factory

from loxone.apps.measurements.models import Measurement
from . import BuildingFactory
import random


class MeasurementFactory(factory.django.DjangoModelFactory):
    value = factory.LazyAttribute(lambda a: random.randrange(2000, 3000) / 100)
    type = "temperature"
    time = factory.Sequence(
        lambda n: datetime.combine(datetime.today(), datetime.min.time())
        - timedelta(hours=n + 1)
    )
    url = factory.Sequence(lambda n: "Measurement {0}".format(n + 1))
    zone = factory.Sequence(lambda n: "Zone {0}".format(n + 1))
    building = factory.SubFactory(BuildingFactory)
    status = "active"

    class Meta:
        model = Measurement
