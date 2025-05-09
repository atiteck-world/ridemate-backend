
from django.urls import path
from .views import RideCreateView, RideListView, RideDetailView, BookRideView, MyBookingsView, CancelBookingView, DriverRideBookingView, UserNotificationView

urlpatterns = [
    path('create/', RideCreateView.as_view(), name='ride-create'),
    path('list/', RideListView.as_view(), name='ride-list'),
    path('<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('<int:ride_id>/book/', BookRideView.as_view(), name='book-ride'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('cancel-booking/<int:pk>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('driver/bookings/', DriverRideBookingView.as_view(), name='driver-ride-bookings'),
    path('notifications/', UserNotificationView.as_view(), name='user-notifications'),
]