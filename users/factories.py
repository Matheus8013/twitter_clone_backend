import factory
from django.contrib.auth.hashers import make_password # Importe para hashear a senha
from .models import User # Importe seu User model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',) # Se o username for único, evite criar duplicados no teste
        skip_postgeneration_save = True

    # Campos básicos do AbstractUser
    username = factory.Sequence(lambda n: f"user{n}") # Gera usernames únicos (user0, user1, etc.)
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com") # E-mail baseado no username
    first_name = factory.Faker('first_name') # Gera nomes aleatórios
    last_name = factory.Faker('last_name')   # Gera sobrenomes aleatórios

    # Campo de senha - importante hashear!
    # factory.PostGeneration é usado para chamar uma função DEPOIS que o objeto foi criado.
    # No caso, após o usuário ser salvo, definimos a senha com make_password.
    password = factory.PostGenerationMethodCall('set_password', 'SenhaF0rtePraTestes!') # Senha padrão para testes