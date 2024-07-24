from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import AppRegistryNotReady
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


from .models import Booking, Vehicle
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer


def export_bookings_xls(request):
    try:
        # Import and class creation here to avoid circular import and handle AppRegistryNotReady exception
        from .models import Booking
        from import_export import resources

        
        class BookingResource(resources.ModelResource):
            class Meta:
                model = Booking

        booking_resource = BookingResource()
        dataset = booking_resource.export()
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="bookings.xls"'
        return response
    except AppRegistryNotReady:
        return HttpResponse("Application is not ready. Please try again.")


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=True, methods=['post'])
    def associate_vehicle(self, request, pk=None):
        booking = self.get_object()
        vehicle_id = request.data.get('vehicle_id')
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.booking = booking
            vehicle.save()
            return Response({'status': 'Vehicle associated successfully'})
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=404)

    @action(detail=True, methods=['post'])
    def disassociate_vehicle(self, request, pk=None):
        booking = self.get_object()
        vehicle_id = request.data.get('vehicle_id')
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id, booking=booking)
            vehicle.booking = None
            vehicle.save()
            return Response({'status': 'Vehicle disassociated successfully'})
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found or not associated with this booking'}, status=404)

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
