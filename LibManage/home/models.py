from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    available = models.CharField(max_length=50)
    summary = models.TextField()
    def __str__(self):
        return self.title 


# the 2 lines above are written so that name of book is displayed in the admin portal

# to detect changes 2 tasks have to be done
# first you have to register your model, in admin.py
# second, register your app, in settings.py

# when we run makemigrations, the database table is not created, but a file having the above changes is made
# the database table is created on running migrate command