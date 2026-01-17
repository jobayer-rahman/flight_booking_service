from django.contrib import admin
from .models import (
    Airline,
    Airport,
    Booking,
    City,
    Country,
    Flight,
    Author,
    Book
)


admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Booking)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Flight)
admin.site.register(Author)
admin.site.register(Book)