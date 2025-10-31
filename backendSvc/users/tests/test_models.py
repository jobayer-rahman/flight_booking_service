from ..models import User
from django.test import TestCase
from users.factories import SuperUserFactory, UserFactory

class UserModelTests(TestCase):
    def test_default_customer_role(self):
        user = UserFactory()
        self.assertEqual(user.role, User.Roles.CUSTOMER)

    def test_superuser_role(self):
        superuser = SuperUserFactory()
        self.assertEqual(superuser.role, User.Roles.ADMIN)
        self.assertEqual(superuser.is_superuser, True)

    def test_carrier_role(self):
        carrier = UserFactory(role="carrier")
        self.assertEqual(carrier.role, User.Roles.CARRIER)

    def test_admin_role(self):
        admin = UserFactory(role="admin")
        self.assertEqual(admin.role, User.Roles.ADMIN)

    def test_agency_role(self):
        agency = UserFactory(role="agency")
        self.assertEqual(agency.role, User.Roles.AGENCY)