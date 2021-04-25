from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# set of genres
GENRES = (
    ('Humanities & Social Sciences','Humanities & Social Sciences'),
    ('Science & Technology','Science & Technology'),
    ('Fiction','Fiction'),
    ('Romance','Romance'),
    ('Graphic Novel','Graphic Novel'),
    ('Short Story & Essays','Short Story & Essays'),
    ('Poem','Poem'),
    ('Memoir & Autobiography','Memoir & Autobiography'),
    ('Food & Drink','Food & Drink'),
    ('Art & Photography','Art & Photography'),
    ('Self-help & Personal Growth','Self-help & Personal Growth'),
    ('Mythology','Mythology'),
    ('Travel','Travel')
)

STOCK = (
    ('Available','Available'),
    ('Not Available','Not Available')
)

# database object for a book
class Book(models.Model):
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    genre = models.CharField(max_length=50,
                  choices=GENRES,
                  default="Fiction")
    available = models.CharField(max_length=15,
                  choices=STOCK,
                  default="Available")
    quantity = models.IntegerField(default=0)
    summary = models.TextField()
    objects = models.Manager() # this is written because VSC was giving error that class has no objcts
    def __str__(self):
        return self.title 

# databse model for a request to borrow/renew a book
class BookRequest(models.Model):
    user = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    title = models.CharField(max_length=200)  
    author = models.CharField(max_length=200) 
    period=models.IntegerField(default=7) 
    objects = models.Manager()
    def __str__(self):
        str="Title:"+self.title+" ---- User:"+self.user 
        return str

# database model to store the books borrowed from librarry at any time
class BorrowedBook(models.Model):
    user = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=100)
    title = models.CharField(max_length=200) 
    author = models.CharField(max_length=200)
    date=models.DateField()
    due_date=models.DateField()
    period=models.IntegerField()
    objects = models.Manager()
    def __str__(self):
        str="Title:"+self.title+" ---- User:"+self.user 
        return str

ACCOUNT_TYPES = (
    ('librarian','librarian'),
    ('user','user'),
    ('admin','admin')
)

class system_variable_values(models.Model):
    book_lost_penalty_amount=models.IntegerField(default=1000)   # per book
    issue_period_expired_penalty=models.IntegerField(default=10) # per day
    objects = models.Manager()


# this adds account_type field to the user object of django
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=9,
                  choices=ACCOUNT_TYPES,
                  default="user")
    penalty = models.IntegerField(default=0)
    objects = models.Manager()
    def __str__(self):
        return self.user.username 


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Comments for self help 
# to detect changes 2 tasks have to be done
# first you have to register your model, in admin.py
# second, register your app, in settings.py

# when we run makemigrations, the database table is not created, but a file having the above changes is made
# the database table is created on running migrate command