from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('book', views.bookpage, name='bookpage'),
    path('addBook', views.addBook, name='addBook'),

]
