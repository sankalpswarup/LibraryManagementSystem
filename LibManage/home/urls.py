from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from home import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('all_books', views.all_books, name='all_books'),
    path('profile', views.profile, name='profile'),
    path('addBook', views.addBook, name='addBook'),
    path('register', views.register, name='register'),
    path('login_user', views.loginUser, name='login_user'),
    path('bookpage', views.bookpage, name='bookpage'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('edit_book', views.edit_book, name='edit_book'),
    path('change_access', views.change_access, name='change_access'),
    path('book_returned', views.book_returned, name='book_returned'),
    path('borrow_book', views.borrow_book, name='borrow_book'),
    path('request_accepted', views.request_accepted, name='request_accepted'),
    path('request_rejected', views.request_rejected, name='request_rejected'),
    path('log', views.log, name='log'),
    path('book_edited', views.book_edited, name='book_edited'),
    path('sort_genre', views.sort_genre, name='sort_genre'),
    path('searched_book', views.searched_book, name='searched_book'),
    path('searched_author', views.searched_author, name='searched_author'),
    path('renew_period', views.renew_period, name='renew_period'),
    path('book_lost', views.book_lost, name='book_lost'),


    

]
