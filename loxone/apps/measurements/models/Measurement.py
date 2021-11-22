from django.db import models

from loxone.core.models import BaseModel
from ..managers import MeasurementManager


class Measurement(BaseModel):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=100)
    time = models.DateTimeField(null=True)
    url = models.CharField(max_length=1500)
    zone = models.CharField(max_length=1500)
    building = models.ForeignKey("measurements.Building", on_delete=models.RESTRICT)
    objects = MeasurementManager()

    class Meta:
        ordering = ["-created"]
        default_related_name = "measurements"
        indexes = [
            models.Index(fields=["created"]),
        ]
        unique_together = [["building", "url", "time", "type"]]

    def __str__(self):
        return str(self.value)
