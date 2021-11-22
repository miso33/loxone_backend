from rest_framework.serializers import ModelSerializer
from .models import Measurement


class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = ["value", "type", "time", "url", "zone", "building"]
