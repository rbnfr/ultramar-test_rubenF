from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import Vehicle

class Command(BaseCommand):
    help = 'Delete vehicles with booking ship arrival date older than 6 months'

    def handle(self, *args, **kwargs):
        six_months_ago = timezone.now().date() - timedelta(days=180)
        old_vehicles = Vehicle.objects.filter(booking__ship_arrival_date__lt=six_months_ago)
        count = old_vehicles.count()
        old_vehicles.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old vehicles'))