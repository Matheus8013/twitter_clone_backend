# follow/tests/test_follow.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from follow.models import Follow
from follow.factories import FollowFactory
from users.factories import UserFactory


class FollowViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()
        self.follow_url = reverse('follow:follow-list')
        self.client.force_authenticate(user=self.user1)

    def test_follow_creation(self):
        data = {'following': self.user2.id}
        response = self.client.post(self.follow_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_unfollow(self):
        follow = FollowFactory(follower=self.user1, following=self.user2)
        follow_detail_url = reverse('follow:follow-detail', args=[follow.pk])
        response = self.client.delete(follow_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 0)

    def test_followers_list(self):
        FollowFactory(follower=self.user1, following=self.user2)
        FollowFactory(follower=self.user3, following=self.user2)

        self.client.force_authenticate(user=self.user2)
        followers_url = reverse('follow:follow-user-followers')
        response = self.client.get(followers_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        follower_usernames = [f['follower_username'] for f in response.data['results']]
        self.assertIn(self.user1.username, follower_usernames)
        self.assertIn(self.user3.username, follower_usernames)

    def test_following_list(self):
        FollowFactory(follower=self.user1, following=self.user2)
        FollowFactory(follower=self.user1, following=self.user3)

        following_url = reverse('follow:follow-user-following')
        response = self.client.get(following_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Acessa a lista de resultados usando a chave 'results'
        self.assertEqual(len(response.data['results']), 2)
        following_usernames = [f['following_username'] for f in response.data['results']]
        self.assertIn(self.user2.username, following_usernames)
        self.assertIn(self.user3.username, following_usernames)

