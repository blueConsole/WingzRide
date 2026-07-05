from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer
from django.db.models import ExpressionWrapper, F, FloatField, Value, Prefetch
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Sqrt
from .permissions import IsAdmin
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class RideViewSet(ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdmin]  
    def get_queryset(self):
        today = timezone.now() - timedelta(hours=24)
        todays_events = RideEvent.objects.filter(created_at__gte=today)
        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch('events', queryset=todays_events, to_attr='todays_events')
        )
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

            if pickup_latitude is None or pickup_longitude is None:
                raise ValidationError({
                    'ordering': 'pickup_latitude and pickup_longitude are required when ordering=distance.'
                })

            try:
                pickup_latitude = float(pickup_latitude)
                pickup_longitude = float(pickup_longitude)
            except ValueError:
                raise ValidationError({
                    'pickup_latitude': 'A valid number is required.',
                    'pickup_longitude': 'A valid number is required.',
                })

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
        elif ordering is not None:
            raise ValidationError({
                'ordering': 'Supported values are pickup_time, -pickup_time, and distance.'
            })
        else:
            queryset = queryset.order_by('id_ride')
        return queryset

class RideEventViewSet(ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdmin]
