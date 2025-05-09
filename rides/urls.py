
from django.urls import path
from .views import BookingApprovalView, ChatThreadView, DriverRatingListView, InboxView, RideCreateView, RideHistoryView, RideListView, RideDetailView, BookRideView, MyBookingsView, CancelBookingView, DriverRideBookingView, SendMessageView, SubmitRatingView, UserNotificationView

urlpatterns = [
    path('create/', RideCreateView.as_view(), name='ride-create'),
    path('list/', RideListView.as_view(), name='ride-list'),
    path('<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('<int:ride_id>/book/', BookRideView.as_view(), name='book-ride'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('cancel-booking/<int:pk>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('driver/bookings/', DriverRideBookingView.as_view(), name='driver-ride-bookings'),
    path('bookings/<int:booking_id>/status/', BookingApprovalView.as_view(), name='booking-approval'),
    path('notifications/', UserNotificationView.as_view(), name='user-notifications'),
    path('submit-rating/', SubmitRatingView.as_view(), name='submit-rating'),
    path('drivers/<int:driver_id>/ratings/', DriverRatingListView.as_view(), name='driver-ratings'),
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/thread/<int:user_id>/', ChatThreadView.as_view(), name='chat-thread'),
    path('messages/inbox/', InboxView.as_view(), name='inbox'),
    path('history/', RideHistoryView.as_view(), name='ride-history'),
]