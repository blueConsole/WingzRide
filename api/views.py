from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer
from django.db.models import ExpressionWrapper, F, FloatField, Value
from django.db.models.functions import Sqrt

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
        elif ordering == 'distance':
            pickup_latitude = self.request.query_params.get('pickup_latitude', None)
            pickup_longitude = self.request.query_params.get('pickup_longitude', None)

            if pickup_latitude is not None and pickup_longitude is not None:
                pickup_latitude = float(pickup_latitude)
                pickup_longitude = float(pickup_longitude)

                latitude_difference = F('pickup_latitude') - Value(pickup_latitude)
                longitude_difference = F('pickup_longitude') - Value(pickup_longitude)
                distance_expression = (
                    latitude_difference * latitude_difference
                ) + (
                    longitude_difference * longitude_difference
                )

                queryset = queryset.annotate(
                    distance=ExpressionWrapper(
                        Sqrt(distance_expression),
                        output_field=FloatField()
                    )
                ).order_by('distance')
        return queryset

class RideEventViewSet(ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
