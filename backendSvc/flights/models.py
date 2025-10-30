from django.db import models
from users.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name

class City(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name
    

class Airport(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='airports', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.code}"

class Airline(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flight(BaseModel):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, related_name='flights', on_delete=models.CASCADE)
    deprature = models.ForeignKey(Airport, related_name='departures', on_delete=models.CASCADE)
    arrival = models.ForeignKey(Airport, related_name='arrivals', on_delete=models.CASCADE)
    deprature_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)

class Booking(BaseModel):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        PENDING = "pending", "Pending"
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, related_name='bookings', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats_booked = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    
    class Meta:
        unique_together = ('user', 'flight')
    
    def __str__(self):
        return f"{self.user} -- {self.flight.flight_number}"
    
    