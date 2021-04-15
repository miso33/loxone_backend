from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions

from .tracking import TrackingView
from ..paginations import BasePagination


class BaseView(TrackingView, ModelViewSet):
    pagination_class = BasePagination
    permission_classes = (DjangoModelPermissions,)
