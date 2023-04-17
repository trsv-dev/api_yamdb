from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404
from rest_framework import filters
from api.filters import TitleFilter

from reviews.models import User, Category, Genre, Title, Review, Comment


from api.serializers import (ReviewSerializer, CommentSerializer,
                             CategorySerializer, GenreSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             AllcomentsSerializer, UserSerializer)
from api.mixins import CreateDestroyListViewSet

from rest_framework.response import Response
from api.permissions import AdminUserOrReadOnly, AdminUserOnly, AdminUser
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api_yamdb.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import AccessToken

from api import serializers
from django.contrib.auth.tokens import (default_token_generator,
                                        PasswordResetTokenGenerator)




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
    #permission_classes = (IsAuthenticatedOrReadOnly,)
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

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()
    
    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(review_id=review_id, author=self.request.user)


class CustomSignUp(generics.CreateAPIView, PasswordResetTokenGenerator):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data['email']
            try:
                user, _ = User.objects.get_or_create(email=email,
                                                     username=username)
            except IntegrityError:
                raise ValidationError

            confirmation_code = default_token_generator.make_token(user)
            message = (f'Здравствуйте, {username}!'
                       f' Это ваш код подтверждения {confirmation_code}')
            send_mail(
                'Код подтверждения',
                message,
                EMAIL_HOST_USER,
                [email]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(generics.ListCreateAPIView):
    serializer_class = serializers.ConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response({'token': str(token)},
                                status=status.HTTP_200_OK)
        else:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminUser, IsAuthenticated)



class UserViewSetMe(generics.RetrieveAPIView, UpdateAPIView):
    serializers_class = UserSerializer

    def get(self, request):
        queryset = User.objects.filter(user=self.request.user)
        return queryset


