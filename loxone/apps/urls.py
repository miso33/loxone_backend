from rest_framework.routers import DefaultRouter
from .buildings.views import BuildingViewSet
from .measurements.views import MeasurementViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'measurements', MeasurementViewSet)
urlpatterns = router.urls
