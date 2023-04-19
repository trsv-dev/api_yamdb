from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        help_text='Укажите название категории'
    )
    slug = models.SlugField(
        unique=True,
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимый символ в slug'
            ),
        ),
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
        validators=(
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимый символ в slug'
            ),
        ),
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
        max_length=100,
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
        blank=True,
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
            MinValueValidator(
                1, message='Оценка должна быть от 1 до 10'
            ),
            MaxValueValidator(
                10, message='Оценка должна быть от 1 до 10'
            )
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
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
