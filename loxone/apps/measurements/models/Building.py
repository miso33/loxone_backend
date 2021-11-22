from django.db import models

from loxone.core.models import BaseModel


class Building(BaseModel):
    name = models.CharField(max_length=200, unique=True, verbose_name="Názov")
    url = models.CharField(max_length=500, unique=True)
    login = models.CharField(max_length=500)
    password = models.CharField(max_length=500, verbose_name="Heslo")

    class Meta:
        ordering = ["name"]
        default_related_name = "buildings"
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Budova"
        verbose_name_plural = "Budovy"

    def __str__(self):
        return str(self.name)
