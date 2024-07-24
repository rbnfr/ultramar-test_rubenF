from rest_framework import serializers
from .models import Booking, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vin', 'make', 'model', 'weight', 'booking']

class BookingSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date', 'vehicles']