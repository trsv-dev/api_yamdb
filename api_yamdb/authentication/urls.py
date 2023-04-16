from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.CustomSignUp.as_view() , name='signup' ),
    path('token', views.GetToken.as_view(), name='token')
]