from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)
router.register(r'vehicles', views.VehicleViewSet)

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('bookings/<int:booking_pk>/associate/<int:vehicle_pk>/',
         views.VehicleAssociationView.as_view(), name='associate_vehicle'),
    path('bookings/<int:booking_pk>/dissociate/<int:vehicle_pk>/',
         views.VehicleDisassociationView.as_view(), name='disassociate_vehicle'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('api/', include(router.urls)),
    path('export/bookings/xls/', views.export_bookings_xls, name='export_bookings_xls'),
]
