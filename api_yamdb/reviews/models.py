from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from reviews.validators import username_validator
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    confirmation_code = models.CharField(
        max_length=250,
        default='-Пусто-',
        blank=False,
        null=True,
        verbose_name='Код подтверждения',
        help_text='Введите код подтверждения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Категория',
        help_text='Укажите название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='URL',
        help_text='Укажите URL категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Жанр',
        help_text='Укажите название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='URL',
        help_text='Укажите URL жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Укажите название'
    )
    year = models.IntegerField(
        validators=(
            MaxValueValidator(
                int(datetime.now().year),
                message='Нельзя указать год в будущем'
            ),
        ),
        verbose_name='Год',
        help_text='Укажите год'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Укажите категорию'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
        help_text='Укажите жанр произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Опишите произведение',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def update_rating(self):
        self.rating = self.reviews.aggregate(Avg("score"))["score__avg"] or 0
        self.save()

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )

    class Meta:
        verbose_name = '"Связь" жанр/произведение'
        verbose_name_plural = '"Связь" жанры/произведения'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Введите текст',
        help_text='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Выберите автора'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Оцените от 1 до 10',
        validators=(
            MinValueValidator(1, message='Оценка должна быть от 1 до 10'),
            MaxValueValidator(10, message='Оценка должна быть от 1 до 10')
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    rating = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения.',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
    
    def average_rating(self) -> float:
        return Review.objects.filter(title=self.title).aggregate(Avg("score"))["score__avg"] or 0
        

    def save(self, *args, **kwargs):
        self.rating = self.average_rating()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Отзыв {self.author} на "{self.title}"'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Выберите отзыв'
    )
    text = models.TextField(
        verbose_name='Введите текст',
        help_text='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} прокомментировал {self.review}'
