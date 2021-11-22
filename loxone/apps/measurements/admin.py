from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from loxone.core.admin import BaseAdmin, BaseStatusAdmin
from .models import Building, Measurement


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
    list_display = ("name", "url") + BaseStatusAdmin.list_display
    actions = [make_active, make_inactive]

    def get_queryset(self, request):
        return Building.all_objects.all()


class ZoneFilter(admin.SimpleListFilter):
    title = "Zóny"
    parameter_name = "zone"

    def lookups(self, request, model_admin):
        filters = {}
        if "type" in request.GET:
            filters["type"] = request.GET["type"]
        if "building" in request.GET:
            filters["type"] = request.GET["building"]
            zones = list(
                dict.fromkeys(
                    list(
                        Measurement.objects.filter(
                            building__name=request.GET["building"]
                        ).order_by(
                            "zone"
                        ).values_list(
                            "zone"
                        )
                    )
                )
            )
            zones_for_filter = []
            for zone in zones:
                zones_for_filter.append((zone[0], zone[0]))
            return tuple(zones_for_filter)
        return tuple()

    def queryset(self, request, queryset):
        if "building__id__exact" in request.GET and "zone" in request.GET:
            return queryset.filter(
                zone=request.GET["zone"], building=request.GET["building__id__exact"]
            )
        return queryset.all()


class BuildingFilter(admin.SimpleListFilter):
    title = "Predajne"
    parameter_name = "building"

    def lookups(self, request, model_admin):
        buildings_for_filter = []
        filters = {}
        if "type" in request.GET:
            filters["measurements__type"] = request.GET["type"]
        for building in (
                Building.objects.filter(**filters).order_by(
                    "name"
                ).values_list(
                    "name",
                    flat=True
                ).distinct()
        ):
            buildings_for_filter.append((building, building))
        return tuple(buildings_for_filter)

    def queryset(self, request, queryset):
        filters = {}
        if "building" in request.GET:
            filters["building__name"] = request.GET["building"]
        if "building" in request.GET and "zone" in request.GET:
            if Measurement.objects.filter(
                    zone=request.GET["zone"], building__name=request.GET["building"]
            ):
                filters["zone"] = request.GET["zone"]
        return queryset.filter(**filters)


class MeasurementAdmin(BaseAdmin):
    list_display = ("value", "time", "type", "zone", "building")
    list_filter = ("type", BuildingFilter, ZoneFilter, ("time", DateRangeFilter))
    list_editable = ("time",)

    def get_queryset(self, request):
        return Measurement.all_objects.all()


admin.site.register(Building, BuildingAdmin)
admin.site.register(Measurement, MeasurementAdmin)
