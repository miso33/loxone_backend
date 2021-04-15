from django.db import models

from apps.core.models import BaseModel


class Measurement(BaseModel):
    value = models.DecimalField(max_digits=3, decimal_places=2)
    type = models.CharField(max_length=5)
    time = models.DateTimeField()
    url = models.CharField(max_length=500)
    zone = models.CharField(max_length=500)
    building = models.ForeignKey('stats.Building', on_delete=models.RESTRICT)

    class Meta:
        ordering = ['-created']
        default_related_name = 'measurements'
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return self.id
