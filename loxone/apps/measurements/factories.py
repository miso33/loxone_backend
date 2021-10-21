import factory

from .models import Measurement


class MeasurementFactory(factory.django.DjangoModelFactory):
    value = factory.Sequence(lambda n: {0}.format((n + 1) / 10))
    type = factory.Sequence(lambda n: 'Measurement {0}'.format(n + 1))
    time = factory.Sequence(lambda n: datetime.datetime.now() - timedelta(minutes=n + 1))
    url = factory.Sequence(lambda n: 'Measurement {0}'.format(n + 1))
    zone = factory.Sequence(lambda n: 'Measurement {0}'.format(n + 1))
    building = factory.SubFactory(BuildingFactory)
    status = 'active'

    class Meta:
        model = Measurement
