from rest_framework import viewsets

from reviews.models import User, Category, Genre, Title, Review, Comment


class Auth:  # надо придумать от чего наследовать
    """
    Получить код подтверждения на переданный email,
    получение JWT-токена в обмен на username и confirmation code.
    """
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    Получить список всех пользователей,
    добавить нового пользователя,
    получить пользователя по username,
    изменить данные пользователя по username,
    удалить пользователя по username,
    получить данные своей учетной записи по (англ.) me,
    изменить данные своей учетной записи по (англ.) me.
    """
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Получить список всех категорий,
    создать категорию,
    удалить категорию.
    """
    pass


class GenreViewSet(viewsets.ModelViewSet):
    """
    Получить список всех жанров,
    добавить жанр,
    удалить жанр.
    """
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех произведений,
    добавить новое произведение,
    получение информации о произведении,
    частичное обновление информации о произведении,
    удаление произведения.
    """
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получить список отзывов,
    получить один отзыв по id,
    добавить отзыв по id,
    частично обновить отзыв по id,
    удалить отзыв по id.
    """
    pass


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить список всех комментариев к отзыву по id,
    добавить новый комментарий для отзыва,
    получить комментарий для отзыва по id,
    частично обновить комментарий к отзыву по id,
    удалить комментарий к отзыву по id.
    """
    pass
