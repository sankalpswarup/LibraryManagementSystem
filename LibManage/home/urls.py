from django.contrib import admin
from django.urls import path, re_path
# from django.conf.urls import url
# from django.conf.urls import re_path
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
    path('book_returned', views.book_returned, name='book_returned'),
    path('borrow_book', views.borrow_book, name='borrow_book'),
    path('request_accepted', views.request_accepted, name='request_accepted'),
    path('request_rejected', views.request_rejected, name='request_rejected'),
    path('log', views.log, name='log'),
    path('book_edited', views.book_edited, name='book_edited'),
    path('book_searched', views.book_searched, name='book_searched'),
    path('renew_period', views.renew_period, name='renew_period'),
    path('book_lost', views.book_lost, name='book_lost'),
    path('display_users', views.display_users, name='display_users'),
    path('penalty_returned', views.penalty_returned, name='penalty_returned'),
    path('change_account_type', views.change_account_type, name='change_account_type'),
    path('delete_book', views.delete_book, name='delete_book'),
    path('issue_book', views.issue_book, name='issue_book'),
    path('update_penalty_amount', views.update_penalty_amount, name='update_penalty_amount'),


    

]
