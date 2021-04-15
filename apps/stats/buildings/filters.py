import rest_framework_filters as filters

from apps.core.filters import BaseFilter
from .models import Building


class BuildingFilter(BaseFilter):
    pass
    
    class Meta:
        model = Building
        fields = ['name', 'url', 'login', 'password']
