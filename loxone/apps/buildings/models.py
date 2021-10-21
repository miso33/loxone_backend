from django.db import models

from loxone.core.models import BaseModel
from loxone.apps.buildings.managers import BuildingManager


class Building(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=500, unique=True)
    login = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    objects = BuildingManager()

    class Meta:
        ordering = ['-created']
        default_related_name = 'buildings'
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return str(self.name)
