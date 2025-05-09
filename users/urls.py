from django.urls import path
from .views import DriverListView, DriverProfileView, PassengerProfileView, PublicDriverProfileView, RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('driver-profile/', DriverProfileView.as_view(), name='driver-profile'),
    path('passenger-profile/', PassengerProfileView.as_view(), name='passenger-profile'),
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/<int:user_id>/', PublicDriverProfileView.as_view(), name='public-driver-profile'),
]
