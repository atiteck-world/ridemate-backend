
from django.urls import path
from .views import RideCreateView, RideListView, RideDetailView

urlpatterns = [
    path('create/', RideCreateView.as_view(), name='ride-create'),
    path('list/', RideListView.as_view(), name='ride-list'),
    path('<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
]