from django.db import models

from loxone.core.models import BaseModel
from ..managers import MeasurementManager


class Measurement(BaseModel):
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Hodnota")
    type = models.CharField(max_length=100, verbose_name="Typ")
    time = models.DateTimeField(null=True, verbose_name="Čas a dátmum")
    url = models.CharField(max_length=1500)
    zone = models.CharField(max_length=1500, verbose_name="Zóna")
    building = models.ForeignKey("measurements.Building", on_delete=models.RESTRICT, verbose_name="Budova")
    objects = MeasurementManager()

    class Meta:
        ordering = ["-created"]
        default_related_name = "measurements"
        verbose_name = "Meranie"
        verbose_name_plural = "Merania"
        indexes = [
            models.Index(fields=["created"]),
        ]
        unique_together = [["building", "url", "time", "type"]]

    def __str__(self):
        return str(self.value)
