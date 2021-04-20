from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    available = models.CharField(max_length=50)
    summary = models.TextField()
    objects = models.Manager() # this is written because VSC was giving error that class has no objcts
    def __str__(self):
        return self.title 
class BookRequest(models.Model):
    user = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    title = models.CharField(max_length=200)  
    author = models.CharField(max_length=200)  
    objects = models.Manager()
    def __str__(self):
        str="Title:"+self.title+" ---- User:"+self.user 
        return str

class BorrowedBook(models.Model):
    user = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    title = models.CharField(max_length=200) 
    author = models.CharField(max_length=200)
    objects = models.Manager()
    def __str__(self):
        str="Title:"+self.title+" ---- User:"+self.user 
        return str

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.TextField(max_length=50) # this will store user/librarian
                                                   # this can be modified to some other field more apt for it
    objects = models.Manager()
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    

# the 2 lines above are written so that name of book is displayed in the admin portal

# to detect changes 2 tasks have to be done
# first you have to register your model, in admin.py
# second, register your app, in settings.py

# when we run makemigrations, the database table is not created, but a file having the above changes is made
# the database table is created on running migrate command