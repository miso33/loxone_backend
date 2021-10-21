from django.contrib.auth import get_user_model

from loxone.core.views import BaseView
from loxone.core.permissions import ViewDjangoModelPermission
from .filters import UserFilter
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(BaseView):
    filter_class = UserFilter
    queryset = User.objects.filter()
    permission_classes = (ViewDjangoModelPermission,)
    serializer_class = UserSerializer

