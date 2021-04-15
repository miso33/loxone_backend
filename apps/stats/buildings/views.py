from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.core.views import BaseView
from .serializers import BuildingSerializer
from .models import Building
from .filters import BuildingFilter


class BuildingViewSet(BaseView):
    filter_class = BuildingFilter
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    