import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from users.factories import UserFactory
from .models import Post, Like, Comment

User = get_user_model()

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    content = factory.Faker('text', max_nb_chars=200)

class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    content = factory.Faker('text', max_nb_chars=200)