from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posts.models import Like
from posts.factories import UserFactory, PostFactory, LikeFactory

class LikeViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.post = PostFactory(author=self.user2)
        self.like_url = reverse('posts:likes-list')
        self.client.force_authenticate(user=self.user1)

    def test_like_creation(self):
        data = {'post': self.post.id}
        response = self.client.post(self.like_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())

    def test_like_deletion(self):
        like = LikeFactory(user=self.user1, post=self.post)
        like_detail_url = reverse('posts:likes-detail', args=[like.id])
        response = self.client.delete(like_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_unique_like_constraint(self):
        LikeFactory(user=self.user1, post=self.post)
        data = {'post_id': self.post.id}
        response = self.client.post(self.like_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)