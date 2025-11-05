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

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        password = extracted #  or "defaultpassword123"
        self.set_password(password)
        self.save()

class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True