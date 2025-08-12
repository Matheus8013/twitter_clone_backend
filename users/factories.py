import factory
from .models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Adicione esta linh
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if create and extracted:
            self.set_password(extracted)
            self.save()
        elif create and not extracted:
            self.set_password('SenhaF0rtePraTestes!')
            self.save()