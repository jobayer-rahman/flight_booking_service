from ..models import User
from django.test import TestCase

class UserModelTests(TestCase):
    def test_default_customer_role(self):
        data = {
            "username": "test_user",
            "password": "test@1234",
            "msisdn": "123456"
        }
        user = User.objects.create_user(**data)
        self.assertEqual(user.role, User.Roles.CUSTOMER)

    def test_superuser_role(self):
        data = {
            "username": "admin",
            "password": "admin@1234",
            "msisdn": "99999999"
        }
        superuser = User.objects.create_superuser(**data)
        self.assertEqual(superuser.role, User.Roles.ADMIN)
        self.assertEqual(superuser.is_superuser, True)

    def test_carrier_role(self):
        data = {
            "username": "carrier",
            "password": "carrier@4321",
            "msisdn": "34567890",
            "role": "carrier"
        }
        carrier = User.objects.create_user(**data)
        self.assertEqual(carrier.role, User.Roles.CARRIER)

    def test_admin_role(self):
        data = {
            "username": "admin",
            "password": "admin@4321",
            "msisdn": "34567890",
            "role": "admin"
        }
        admin = User.objects.create_user(**data)
        self.assertEqual(admin.role, User.Roles.ADMIN)

    def test_agency_role(self):
        data = {
            "username": "agency",
            "password": "agency@4321",
            "msisdn": "34567890",
            "role": "agency"
        }
        agency = User.objects.create_user(**data)
        self.assertEqual(agency.role, User.Roles.AGENCY)