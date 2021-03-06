"""test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include

from news.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/news/', NewListCreate.as_view()),
    path('api/new/<int:pk>', NewRetrieveUpdateDestroy.as_view()),
    path('api/new/<int:pk>/vote/', VoteCreateDestroy.as_view()),
    path('api/new/<int:pk>/comments/', CommentListCreate.as_view()),
    path('api/comment/<int:pk>', CommentRetrieveUpdateDestroy.as_view()),


# Auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/signup', signup),
    path('api/login', login),
]