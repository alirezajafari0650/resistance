from rest_framework.routers import DefaultRouter

from broadcast.api.views import BroadcastViewSet, AttachedFileViewSet

router = DefaultRouter()
router.register(r'broadcasts', BroadcastViewSet)
router.register(r'attachedfiles', AttachedFileViewSet)
urlpatterns = router.urls
