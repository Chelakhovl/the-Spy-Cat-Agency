from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet

router = DefaultRouter()
router.register(r'', SpyCatViewSet, basename='cat')

urlpatterns = router.urls