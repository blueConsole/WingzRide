from django.urls import path
from .views import UserViewSet, RideViewSet, RideEventViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('rides/', RideViewSet.as_view({'get': 'list', 'post': 'create'}), name='ride-list'),
    path('ride-events/', RideEventViewSet.as_view({'get': 'list', 'post': 'create'}), name='ride-event-list'),
]