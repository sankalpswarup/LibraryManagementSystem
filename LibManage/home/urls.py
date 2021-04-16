from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('book', views.book, name='book'),
]
