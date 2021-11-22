from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from ..paginations import BasePagination


class BaseView(ModelViewSet):
    pagination_class = BasePagination
    permission_classes = (DjangoModelPermissions,)
