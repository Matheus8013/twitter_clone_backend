import factory
from factory.django import DjangoModelFactory
from follow.models import Follow
from users.factories import UserFactory


class FollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow
        skip_postgeneration_save = True

    follower = factory.SubFactory(UserFactory)
    following = factory.SubFactory(UserFactory)

    @factory.post_generation
    def force_unique_follow(self, create, extracted, **kwargs):
        if create and self.follower == self.following:
            self.follower = UserFactory()
            self.save()