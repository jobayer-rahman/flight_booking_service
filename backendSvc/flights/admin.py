from django.contrib import admin
from .models import (
    Airline,
    Airport,
    Booking,
    City,
    Country,
    Flight,
)


admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Booking)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Flight)