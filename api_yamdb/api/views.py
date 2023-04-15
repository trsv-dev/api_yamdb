from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilter
from reviews.models import User, Category, Genre, Title, Review, Comment


from api.serializers import (ReviewSerializer, CommentSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             AllcomentsSerializer)
from api.mixins import CreateDestroyListViewSet

from rest_framework.response import Response
from api.permissions import AdminUserOrReadOnly


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


class CategoryViewSet(CreateDestroyListViewSet):
    """
    Получить список всех категорий,
    создать категорию,
    удалить категорию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """
    Получить список всех жанров,
    добавить жанр,
    удалить жанр.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех произведений,
    добавить новое произведение,
    получение информации о произведении,
    частичное обновление информации о произведении,
    удаление произведения.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


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
        queryset = Comment.objects.filter(review_id=review_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AllcomentsSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(review_id=review_id, author=self.request.user)
