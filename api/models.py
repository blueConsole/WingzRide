from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=[('rider', 'Rider'), ('driver', 'Driver'), ('admin', 'Admin')])
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=[('en-route', 'En-route'), ('pickup', 'Pickup'), ('dropoff', 'Dropoff'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], db_index=True)
    id_rider = models.ForeignKey(User, related_name='rides_as_a_rider', db_column='id_rider', on_delete=models.PROTECT)
    id_driver = models.ForeignKey(User, related_name='rides_as_a_driver', db_column='id_driver', on_delete=models.PROTECT)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"Ride {self.id_ride} - {self.status}"

class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, related_name='events', db_column='id_ride', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Ride Event {self.id_ride_event} - {self.description}"