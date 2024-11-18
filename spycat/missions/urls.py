from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r'', MissionViewSet, basename='mission')
router.register(r'', TargetViewSet, basename='target')

urlpatterns = router.urls