from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posts.models import Post
from posts.factories import UserFactory, PostFactory
from follow.factories import FollowFactory


class PostViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()
        self.post_url = reverse('posts:post-feed')
        self.client.force_authenticate(user=self.user1)

    def test_post_creation(self):
        create_url = reverse('posts:posts-list')
        data = {'content': 'Este é um post de teste.'}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().author, self.user1)

    def test_post_listing_feed(self):
        PostFactory(author=self.user1)
        PostFactory(author=self.user2)
        PostFactory(author=self.user3)

        FollowFactory(follower=self.user1, following=self.user2)

        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        author_usernames = [post['author_username'] for post in response.data['results']]
        self.assertIn(self.user1.username, author_usernames)
        self.assertIn(self.user2.username, author_usernames)
        self.assertNotIn(self.user3.username, author_usernames)

    def test_post_deletion(self):
        post = PostFactory(author=self.user1)
        delete_url = reverse('posts:posts-detail', args=[post.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_cannot_delete_others_post(self):
        post = PostFactory(author=self.user2)
        post_detail_url = reverse('posts:posts-detail', args=[post.pk])
        response = self.client.delete(post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)