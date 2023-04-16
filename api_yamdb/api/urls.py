from django.urls import path, include
from rest_framework import routers

# в строку ниже надо добавить вьюсет для Auth когда он будет готов
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    UserViewSet, ReviewViewSet, CommentViewSet,
                    CustomSignUp, GetToken)

router = routers.DefaultRouter()

# строку ниже надо изменить после того, как напишем аутентификацию
# пока Auth как заглушка

# router.register(r'auth', Auth, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/signup', CustomSignUp.as_view(), name='signup'),
    path('v1/token', GetToken.as_view(), name='token')
    # path('v1/auth/token', ...),
    # path('v1/auth/signup/', ...),
]
