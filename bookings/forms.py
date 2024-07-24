from django import forms
from .models import Booking, Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['id', 'vin', 'make', 'model', 'weight', 'booking']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date']
        widgets = {
            'ship_arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'ship_departure_date': forms.DateInput(attrs={'type': 'date'}),
        }
