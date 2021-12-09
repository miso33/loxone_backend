from django.contrib import admin

from loxone.core.admin import BaseStatusAdmin
from ..models import Building


@admin.action(description="Aktívna budova")
def make_active(modeladmin, request, queryset):
    # pylint: disable=unused-argument
    queryset.update(status="active")


@admin.action(description="Neaktívna budova")
def make_inactive(modeladmin, request, queryset):
    # pylint: disable=unused-argument
    queryset.update(status="inactive")


class BuildingAdmin(BaseStatusAdmin):
    exclude = ("is_removed",) + BaseStatusAdmin.exclude
    list_display = ("name", "url", "get_recipients", "status")
    actions = [make_active, make_inactive]

    def get_recipients(self, obj):
        return ", ".join([recipient.email for recipient in obj.recipients.filter(is_active=True)])

    def get_queryset(self, request):
        return Building.all_objects.all()


