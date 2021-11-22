from django import template

register = template.Library()


@register.filter(name="building_colspan")
def building_colspan(value):
    return len(value["zone_list"]) * len(value["type_list"]) * 3


@register.filter(name="zone_colspan")
def zone_colspan(value):
    return len(value["type_list"]) * 3


@register.filter(name="type_name")
def type_name(value):
    return {
        "temperature": "Teplota",
        "humidity": "Vlhkosť",
        "CO2": "CO2",
    }[value]
