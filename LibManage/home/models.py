from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    avalability = models.CharField(max_length=50)
    summary = models.TextField()

# to detect cganges 2 tasks have to be done
# first you have to register your model, in admin.py
# second, register your app, in settings.py

# when we run makemigrations, the database table is not created, but a file having the above changes is made
# the database table is created on running migrate command