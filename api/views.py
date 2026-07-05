from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer

# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RideViewSet(ModelViewSet):
    serializer_class = RideSerializer

    def get_queryset(self):
        queryset = Ride.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        rider_email = self.request.query_params.get('rider_email', None)
        if rider_email is not None:
            queryset = queryset.filter(id_rider__email=rider_email)   
        ordering = self.request.query_params.get('ordering', None)
        if ordering in ['pickup_time', '-pickup_time']:
            queryset = queryset.order_by(ordering)
        return queryset

class RideEventViewSet(ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer