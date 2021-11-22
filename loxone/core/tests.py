from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APITestCase, URLPatternsTestCase

from users.factories import UserFactory

User = get_user_model()


class BaseAPITestCase(APITestCase, URLPatternsTestCase):
    def setUp(self):
        if User.Types:
            self.first_user = UserFactory(type=User.Types[0])
            group = Group.objects.get_or_create(name=User.Types[0])
            for p in Permission.objects.all():
                group[0].permissions.add(p)
            self.first_user.groups.add(group[0])
        else:
            self.first_user = UserFactory()
        self.client.force_authenticate(user=self.first_user)
