from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RideViewSet, RideEventViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('rides', RideViewSet)
router.register('ride-events', RideEventViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]