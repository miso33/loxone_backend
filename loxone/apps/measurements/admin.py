from django.contrib import admin

from loxone.core.admin import BaseAdmin
from .models import Measurement


class MeasurementAdmin(BaseAdmin):
    list_display = ('value', 'time', 'type', 'zone')
    list_filter = ('type', 'zone', 'url')

    def get_queryset(self, request):
        return Measurement.all_objects.all()


admin.site.register(Measurement, MeasurementAdmin)
