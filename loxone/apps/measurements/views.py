from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from loxone.core.views import BaseView
# from .filters import MeasurementFilter
from .serializers import MeasurementSerializer
from .models import Measurement


class MeasurementViewSet(BaseView):
    # filter_class = MeasurementFilter
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    # def get_serializer_class(self):
    #     if self.action in ['list', 'retrieve']:
    #         return CautionReadSerializer
    #     return CautionSerializer
    #