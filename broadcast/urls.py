from rest_framework.routers import DefaultRouter

from broadcast.api.views import BroadcastViewSet

router = DefaultRouter()
router.register(r'broadcasts', BroadcastViewSet)
urlpatterns = router.urls
