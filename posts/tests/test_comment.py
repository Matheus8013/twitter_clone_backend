from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from posts.models import Comment
from posts.factories import PostFactory, CommentFactory
from users.factories import UserFactory

class CommentViewSetTests(TestCase):
    def setUp(self):
        print("--- INICIO DO SETUP ---")
        self.client = APIClient()
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.post = PostFactory(author=self.user1)
        self.client.force_authenticate(user=self.user1)

        # Verifique a contagem de comentários antes de criar
        print(f"Comentários antes de criar: {Comment.objects.count()}")

        self.comment1 = CommentFactory(author=self.user1, post=self.post)
        print(f"Comentários depois da 1ª criação: {Comment.objects.count()}")

        self.comment2 = CommentFactory(author=self.user2, post=self.post)
        print(f"Comentários depois da 2ª criação: {Comment.objects.count()}")

        print("--- FIM DO SETUP ---")

    def test_comment_creation(self):
        comment_url = reverse('posts:comments-list')
        data = {
            'post': self.post.id,
            'content': 'Novo comentário de teste.'
        }
        response = self.client.post(comment_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)

    def test_comment_deletion(self):
        comment_detail_url = reverse('posts:comments-detail', args=[self.comment1.id])
        response = self.client.delete(comment_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertFalse(Comment.objects.filter(id=self.comment1.id).exists())

    def test_cannot_delete_others_comment(self):
        comment_detail_url = reverse('posts:comments-detail', args=[self.comment2.id])
        response = self.client.delete(comment_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 2)

    def test_list_comments_for_post(self):
        print("--- TESTE DE LISTAGEM ---")
        # Confirme a contagem no início do teste
        print(f"Comentários no início do teste: {Comment.objects.count()}")

        comments_url = reverse('posts:comments-list')
        response = self.client.get(comments_url, {'post': self.post.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"Comentários no response.data: {len(response.data)}")
        self.assertEqual(len(response.data), 2)