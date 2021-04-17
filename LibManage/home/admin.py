from django.contrib import admin
from home.models import Book

# Register your models here.
admin.site.register(Book)

# by registering the model, they could be seen in the admin page
