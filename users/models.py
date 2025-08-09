from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Model para Usuários
class User(AbstractUser):
    #Adicionar os campos personalizados depois

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=('The groups this user belongs to.'
                    ' A user will get all permissions granted to each of their groups.'
        ),
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name= 'user permissions',
        blank=True,
        help_text= 'The permissions this user has. ',
        related_name='custom_user_permission_set',
        related_query_name='custom_user',
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username