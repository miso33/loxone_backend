from django.contrib import admin

from .buildings.admin import BuildingAdmin, Building
from .measurements.admin import MeasurementAdmin, Measurement

admin.site.register(Building, BuildingAdmin)
admin.site.register(Measurement, MeasurementAdmin)