from django.db import models
from django.db.models import Count, Sum, Avg, F


class BuildingQuerySet(models.QuerySet):
    pass


class BuildingManager(models.Manager):
    def get_queryset(self):
        return BuildingQuerySet(self.model, using=self._db).filter(is_removed=False)

    def statistics(self, building):
        measurement = building.measurements.all()
        measurement.dates('time', 'day').annotate(
            a=F('zone'),
            b=F('type'),
            average_value=Avg('value')
        ).count()
