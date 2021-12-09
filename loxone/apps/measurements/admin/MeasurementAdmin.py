from django.contrib import admin
from import_export import widgets
from import_export.resources import ModelResource, Field
from rangefilter.filters import DateTimeRangeFilter

from loxone.core.admin import BaseAdmin
from ..models import Building, Measurement


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


class BarcodeWidget(widgets.CharWidget):
    def render(self, value, obj):
        type_label = {
            "temperature": "Teplota",
            "humidity": "Vlhkosť",
            "CO2": "CO2",
        }
        if value in type_label:
            return type_label[value]
        else:
            return "unknown"


class ProductGroupsResource(ModelResource):
    type = Field(attribute="type", column_name="Typ", widget=BarcodeWidget())
    building__name = Field(attribute="building__name", column_name="Budova")
    zone = Field(attribute="zone", column_name="Zóna")
    time = Field(attribute="time", column_name="Dátum a čas", widget=widgets.DateWidget("%H:%M:%S %d.%m.%Y"))
    value = Field(attribute="value", column_name="Hodnota")

    def get_queryset(self):
        return self._meta.model.objects.order_by('time')

    class Meta:
        model = Measurement
        fields = ("building__name", "type", "zone", "time", 'value')
        export_order = ("building__name", "type", "zone", "time", 'value')


class MeasurementAdmin(BaseAdmin):
    list_display = ("value", "time", "type", "zone", "building")
    list_filter = ("type", BuildingFilter, ZoneFilter, ("time", DateTimeRangeFilter))
    resource_class = ProductGroupsResource

    def get_queryset(self, request):
        return Measurement.all_objects.all()
