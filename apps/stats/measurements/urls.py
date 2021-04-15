from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'measurements', views.MeasurementViewSet)
urlpatterns = router.urls
