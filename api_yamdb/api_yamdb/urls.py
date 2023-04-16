from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
import json


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('auth/', include('authentication.urls')),
    path('post/', include('reviews.urls')),
]
