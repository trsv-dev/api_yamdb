from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import username_validator, pattern_validator


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        validators=(username_validator, pattern_validator),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Пользователь',
        help_text='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Эл. почта',
        help_text='Введите электронную почту'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
        help_text='Напишите пару фактов из биографии'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию'

    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=150,
        blank=True,
        verbose_name='Роль',
        help_text='Выберите роль'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
