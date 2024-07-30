from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import HttpResponse
from django.core.exceptions import AppRegistryNotReady
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking, Vehicle
from .forms import BookingForm, VehicleForm
from .serializers import BookingSerializer, VehicleSerializer


BOOKING_FORM_TEMPLATE = 'bookings/booking_form.html'
VEHICLE_FORM_TEMPLATE = 'bookings/vehicle_form.html'


def export_bookings_xls():
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


class BookingListView(generic.ListView):
    def get(self, request):
        bookings = Booking.objects.all()
        return render(request, 'bookings/booking_list.html', {'bookings': bookings})


class BookingDetailView(generic.DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_vehicles'] = Vehicle.objects.exclude(booking=self.object)
        return context


class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = BOOKING_FORM_TEMPLATE
    success_url = reverse_lazy('booking_list')


class BookingUpdateView(generic.UpdateView):

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        form = BookingForm(instance=booking)
        return render(request, BOOKING_FORM_TEMPLATE, {'form': form})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_detail', pk=booking.pk)
        return render(request, BOOKING_FORM_TEMPLATE, {'form': form})


class BookingDeleteView(generic.DeleteView):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete()
        return redirect('booking_list')


class VehicleListView(generic.ListView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        return render(request, 'bookings/vehicle_list.html', {'vehicles': vehicles})


class VehicleDetailView(generic.DetailView):
    model = Vehicle
    template_name = 'bookings/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.object
        context['available_bookings'] = Booking.objects.exclude(vehicles=vehicle)
        return context


class VehicleCreateView(generic.CreateView):
    def get(self, request):
        form = VehicleForm()
        return render(request, VEHICLE_FORM_TEMPLATE, {'form': form})

    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
        return render(request, VEHICLE_FORM_TEMPLATE, {'form': form})


class VehicleUpdateView(generic.UpdateView):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(instance=vehicle)
        return render(request, VEHICLE_FORM_TEMPLATE, {'form': form})

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
        return render(request, VEHICLE_FORM_TEMPLATE, {'form': form})


class VehicleDeleteView(generic.DeleteView):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return redirect('vehicle_list')


class VehicleAssociationView(View):
    def post(self, request, booking_pk, vehicle_pk):
        booking = get_object_or_404(Booking, pk=booking_pk)
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
        booking.vehicles.add(vehicle)
        return redirect('booking_detail', pk=booking_pk)


class VehicleDisassociationView(View):
    def post(self, request, booking_pk, vehicle_pk):
        booking = get_object_or_404(Booking, pk=booking_pk)
        vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
        booking.vehicles.remove(vehicle)
        return redirect('booking_detail', pk=booking_pk)


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
