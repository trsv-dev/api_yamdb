from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import uuid

from api_yamdb.settings import EMAIL_HOST_USER
from .validators import username_validator

USER = 'Пользователь'
MODERATOR = 'Модератор'
ADMIN = 'Администратор'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
)


class User(AbstractUser):
    username = models.CharField(
        validators=(username_validator,),
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Пользователь',
        help_text='Имя пользователя'
    )
    email = models.EmailField(
        max_length=200,
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
        max_length=200,
        blank=True,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите фамилию'

    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=50,
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


