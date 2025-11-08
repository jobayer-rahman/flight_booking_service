from django.urls import path
from .views import AirportListAPIView, FlightSearchAPIView

urlpatterns = [
    path('search/', FlightSearchAPIView.as_view(), name='flight-search'),
    path('airports/', AirportListAPIView.as_view(), name='flight-search')
]
