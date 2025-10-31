import factory
from factory.django import DjangoModelFactory
from .models import User
from uuid import uuid4

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    msisdn = factory.Faker("msisdn")

    @factory.lazy_attribute
    def username(self):
        return uuid4().hex[:20]

class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True