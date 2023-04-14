from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import User, Category, Genre, Title, Review, Comment

from api.serializers import ReviewSerializer, CommentSerializer, AllcomentsSerializer
from rest_framework.response import Response


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
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        serializer.save(title_id=title_id, author=self.request.user)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        queryset = Review.objects.filter(title_id=title_id)
        if review_id:
            queryset = queryset.filter(id=review_id)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить список всех комментариев к отзыву по id,
    добавить новый комментарий для отзыва,
    получить комментарий для отзыва по id,
    частично обновить комментарий к отзыву по id,
    удалить комментарий к отзыву по id.
    """
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    queryset = Comment.objects.all()

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        if review_id:
            queryset = Comment.objects.filter(review_id=review_id)
        else:
            queryset = Comment.objects.all()
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AllcomentsSerializer
        return CommentSerializer
    
    
    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(review_id=review_id, author=self.request.user)