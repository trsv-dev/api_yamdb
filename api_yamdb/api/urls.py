from django.urls import path, include
from rest_framework import routers


from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    UserViewSet, ReviewViewSet, CommentViewSet,
                    CustomSignUp, GetToken, UsersViewSet, UserViewSetMe)

router = routers.DefaultRouter()



router.register(r'users', UsersViewSet, basename='users')
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
    path('v1/users/me', UserViewSetMe.as_view(), name='me'),
]
