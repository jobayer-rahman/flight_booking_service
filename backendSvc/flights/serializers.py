from rest_framework import serializers
from .models import (
    Airport,
    Flight,
)


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    country = serializers.CharField(source='city.country.name')

    class Meta:
        model = Airport
        fields = [
            'id',
            'name',
            'code',
            'city',
            'country',
        ]


class FlightSearchSerializer(serializers.ModelSerializer):
    departure_airport = serializers.CharField(source='departure.name')
    arrival_airport = serializers.CharField(source='arrival.name', read_only=True)
    airline_name = serializers.CharField(source='airline.name', read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id',
            'flight_number',
            'airline_name',
            'departure_airport',
            'arrival_airport',
            'departure_time',
            'arrival_time',
            'price',
            'available_seats',
        ]