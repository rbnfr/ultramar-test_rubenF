from django.db import models
from django.core.validators import MinValueValidator


class Booking(models.Model):
    booking_number = models.CharField(max_length=50, unique=True)
    loading_port = models.CharField(max_length=100)
    discharge_port = models.CharField(max_length=100)
    ship_arrival_date = models.DateField()
    ship_departure_date = models.DateField()

    def __str__(self):
        return self.booking_number


class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    weight = models.FloatField(validators=[MinValueValidator(0.0)])
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')

    def __str__(self):
        return self.vin
