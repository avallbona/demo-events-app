from rest_framework.routers import DefaultRouter

from .views import EventApiViewSet

router = DefaultRouter()
router.register("events", EventApiViewSet, basename="event")

urlpatterns = router.urls
