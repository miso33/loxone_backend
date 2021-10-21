from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://localhost:6800')

from .serializers import BuildingSerializer
from .models import Building
from loxone.core.views import BaseView
from loxone.apps.measurements.models import Measurement
from django.core.mail import EmailMessage


class BuildingViewSet(BaseView):  # handles GETs for 1 Company
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    @action(detail=False, methods=['get'])
    def scrape(self, request):
        email = EmailMessage(
            'Hello',
            'Body goes here',
            'labas@scrypta.sk',
            ['mgacko@gmail.com','mkogaci@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        email.send()


        # print(email)
        # # Building.objects.statistics(Building.objects.first())
        # # print(Measurement.objects.list())
        #
        # # for building in self.queryset:
        # building = Building.objects.first()
        # settings = {
        #     'unique_id': "5",
        #     # 'http_user':building.login,
        #     # 'http_pass':building.password,
        # }
        # task = scrapyd.schedule('default', 'StatsSpider',
        #                         settings=settings)

        return Response({}, status=status.HTTP_200_OK)
