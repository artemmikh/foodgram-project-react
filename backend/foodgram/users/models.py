from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """Кастомная модель для User."""

    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        ('user', 'Аутентифицированный пользователь'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    role = models.CharField(
        'Роль пользователя',
        choices=ROLE_CHOICES,
        default='user',
        max_length=20
    )
    confirmation_code = models.CharField('Код подтверждения', max_length=30)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return self.username
