import rest_framework_filters as filters

from apps.core.filters import BaseFilter
from .models import Measurement


class MeasurementFilter(BaseFilter):
    pass
    
    class Meta:
        model = Measurement
        fields = ['value', 'type', 'time', 'url', 'zone', 'building']
