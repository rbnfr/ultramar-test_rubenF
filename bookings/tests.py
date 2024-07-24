import io
from django.test import TestCase, Client
from django.urls import reverse
from .models import Booking
from datetime import date
from openpyxl import load_workbook

class BookingExportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.export_url = reverse('export_bookings_xls')
        
        # Test bookings
        Booking.objects.create(
            booking_number="B001",
            loading_port="Port A",
            discharge_port="Port B",
            ship_arrival_date=date(2023, 1, 1),
            ship_departure_date=date(2023, 1, 5)
        )
        Booking.objects.create(
            booking_number="B002",
            loading_port="Port C",
            discharge_port="Port D",
            ship_arrival_date=date(2023, 2, 1),
            ship_departure_date=date(2023, 2, 5)
        )

    def test_export_bookings_xls(self):
        response = self.client.get(self.export_url)
        
        # Successful response
        self.assertEqual(response.status_code, 200)
        
        # Content type
        self.assertEqual(response['Content-Type'], 'application/vnd.ms-excel')
        
        # Filename
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="bookings.xls"')
        
        wb = load_workbook(filename=io.BytesIO(response.content))
        sheet = wb.active
        
        # Check data
        self.assertEqual(sheet['A2'].value, '1')
        self.assertEqual(sheet['A3'].value, '2')
        self.assertEqual(sheet['B2'].value, 'B001')
        self.assertEqual(sheet['B3'].value, 'B002')
        self.assertEqual(sheet['C2'].value, 'Port A')
        self.assertEqual(sheet['D2'].value, 'Port B')
        self.assertEqual(sheet['C3'].value, 'Port C')
        self.assertEqual(sheet['D3'].value, 'Port D')
        self.assertEqual(sheet['E2'].value, '2023-01-01')
        self.assertEqual(sheet['F2'].value, '2023-01-05')
        self.assertEqual(sheet['E3'].value, '2023-02-01')
        self.assertEqual(sheet['F3'].value, '2023-02-05')