import factory

from ..models import Building


class BuildingFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Building {0}".format(n + 1))
    url = factory.Sequence(lambda n: "Url {0}".format(n + 1))
    login = factory.Sequence(lambda n: "login{0}".format(n + 1))
    password = factory.Sequence(lambda n: "password{0}".format(n + 1))
    status = "active"

    class Meta:
        model = Building
