from django.contrib import admin

from apps.core.admin import BaseAdmin
from .models import Measurement


class MeasurementAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display


    def get_queryset(self, request):
        return Measurement.all_objects.all()


# admin.site.register(Measurement, MeasurementAdmin)
