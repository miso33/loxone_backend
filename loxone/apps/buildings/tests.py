from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from loxone.users.factories import UserFactory
from .factories import BuildingFactory
from .models import Building

User = get_user_model()


class BuildingAPITestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('building/', include('articles.urls')),
    ]

    def setUp(self):
        self.first_user = UserFactory(type=User.Types.MANAGER)
        group = Group.objects.get_or_create(name=User.Types.MANAGER)
        for p in Permission.objects.all():
            group[0].permissions.add(p)
        self.first_user.groups.add(group[0])
        self.client.force_authenticate(
            user=self.first_user
        )
        self.url_list = reverse('building-list')

    
    def test_list(self):
        BuildingFactory.create_batch(10)
        response = self.client.get(path=self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), Building.objects.count())