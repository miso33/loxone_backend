from django.contrib import admin

from loxone.core.admin import BaseStatusAdmin
from .models import Building


class BuildingAdmin(BaseStatusAdmin):
    exclude = ('is_removed',) + BaseStatusAdmin.exclude
    list_display = ('id', 'name', 'url') + BaseStatusAdmin.list_display

    def get_queryset(self, request):
        return Building.all_objects.all()


admin.site.register(Building, BuildingAdmin)
