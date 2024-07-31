from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
)


class User(AbstractUser):
    bio = models.TextField('Биография', null=True, blank=True)
    role = models.CharField(
        'Роль пользователя',
        choices=USER_ROLES,
        max_length=15,
        default=USER_ROLES[0][0]
    )
    confirmation_code = models.PositiveIntegerField(
        'Код подтверждения',
        null=True
    )
    email = models.EmailField(('email address'), unique=True, max_length=254)
