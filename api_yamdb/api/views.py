from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilter
from api.mixins import CreateDestroyListViewSet
from api.permissions import (IsAdminOrReadOnly, IsAuthor,
                             IsModerator, IsAdmin)
from api.serializers import (ReviewSerializer, CommentSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from reviews.models import Category, Genre, Title, Review


class CategoryViewSet(CreateDestroyListViewSet):
    """
    Получить список всех категорий,
    создать категорию,
    удалить категорию.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
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
    queryset = Review.objects.select_related('author', 'title')
    pagination_class = LimitOffsetPagination
    permission_classes = ((IsAuthor | IsModerator | IsAdmin),)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Получить список всех комментариев к отзыву по id,
    добавить новый комментарий для отзыва,
    получить комментарий для отзыва по id,
    частично обновить комментарий к отзыву по id,
    удалить комментарий к отзыву по id.
    """

    serializer_class = CommentSerializer
    permission_classes = ((IsAuthor | IsModerator | IsAdmin),)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.select_related('author')

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
