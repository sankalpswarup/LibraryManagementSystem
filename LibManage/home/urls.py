from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('addBook', views.addBook, name='addBook'),
    path('register', views.register, name='register'),
    path('login_user', views.loginUser, name='login_user'),
    path('bookpage', views.bookpage, name='bookpage'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('edit_book', views.edit_book, name='edit_book'),
    path('change_access', views.change_access, name='change_access'),

]
