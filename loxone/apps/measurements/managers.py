from django.db import models
from django.db.models import Count, Sum, Avg, F, Case, When, DecimalField


class MeasurementQuerySet(models.QuerySet):
    pass


class MeasurementManager(models.Manager):
    def get_queryset(self):
        return MeasurementQuerySet(self.model, using=self._db).filter(is_removed=False)

    def list(self):
        return self.order_by('zone', 'time').distinct('zone', 'time').annotate(
            vlhkost=Case(When(type='H', then=F('value')), output_field=DecimalField()),
            teplota=Case(When(type='T', then=F('value')), output_field=DecimalField())).values('zone', 'time',
                                                                                               'teplota', 'vlhkost')
