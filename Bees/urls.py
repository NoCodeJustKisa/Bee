"""
URL configuration for Bees project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from beehive import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls"), name="log"),
    path('main/', views.mainpage, name="main"),
    path('register/', views.register, name='register'),
    path('create_note/', views.note_creation, name='createnote'),
    path('history/', views.history, name='history'),
    path('history/<int:year>/<int:month>/', views.history, name='history'),
    path('chat/', views.chat, name='chat'),
    path('analytics/', views.analytics, name="analytics"),
    path('home/', views.home, name="home"),
]
