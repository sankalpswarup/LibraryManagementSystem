from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    # path('bookpage', views.bookpage, name='bookpage'),
    path('addBook', views.addBook, name='addBook'),
    path('register', views.register, name='register'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('bookpage', views.bookpage, name='bookpage'),

]
