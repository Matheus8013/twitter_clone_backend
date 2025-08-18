from django.db import models

from users.models import User


# Create your models here.

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} -> {self.following.username}'

    def save(self, *args, **kwargs):
        print("--- NOVO FOLLOW CRIADO ---")
        print(f"Follower: {self.follower.username}, Following: {self.following.username}")
        # Chame o método save original para salvar o objeto
        super().save(*args, **kwargs)
