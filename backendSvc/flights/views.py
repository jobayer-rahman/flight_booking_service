from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.db.models import Q
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .models import Airport, Flight
from .serializers import (
    AirportSerializer,
    FlightSearchSerializer
)


class AirportListAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        airport_list = Airport.objects.select_related('city__country').all()
        if query_params:
            search = query_params.get('search', '').strip()
            airport_list = airport_list.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(city__name__icontains=search) |
                Q(city__country__name__icontains=search)
            )
        serializer = AirportSerializer(airport_list, many=True)
        return Response(serializer.data)


class FlightSearchAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        departure_airport = query_params.get('departure_airport')
        arrival_airport = query_params.get('arrival_airport')
        date = query_params.get('date')

        if not departure_airport or not arrival_airport or not date:
            return Response(
                {"detail": "departure_airport, arrival_airport and date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            search_date = parse_date(date)
            if not search_date:
                raise ValueError
        except ValueError:
            return Response(
                {"detail": "invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        flights = Flight.objects.filter(
            departure_id = departure_airport,
            arrival_id = arrival_airport,
            departure_time__date = search_date,
            available_seats__gt=0
        )

        serializer = FlightSearchSerializer(flights, many=True)
        return Response(serializer.data)