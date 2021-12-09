from django.contrib import admin

from .BuildingAdmin import Building, BuildingAdmin
from .MeasurementAdmin import Measurement, MeasurementAdmin

admin.site.register(Building, BuildingAdmin)
admin.site.register(Measurement, MeasurementAdmin)
