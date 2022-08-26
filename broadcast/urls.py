from rest_framework_mongoengine import routers

from broadcast.api.views import BroadcastViewSet

router = routers.DefaultRouter()
router.register(r'broadcasts', BroadcastViewSet, basename='broadcast')
urlpatterns = router.urls

# urlpatterns += [path('test/', test, name='test')]
