from django.contrib.auth import get_user_model

from core.views import BaseView
from core.permissions import ViewDjangoModelPermission
from .filters import UserFilter
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(BaseView):
    filter_class = UserFilter
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = (ViewDjangoModelPermission,)
    serializer_class = UserSerializer

