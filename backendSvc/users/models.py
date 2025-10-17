from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        CARRIER = "carrier", "Carrier"
        AGENCY = "agency", "Agency"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER
    )
    msisdn = models.CharField(max_length=15)
    is_banned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Roles.ADMIN
        super().save(*args, **kwargs)