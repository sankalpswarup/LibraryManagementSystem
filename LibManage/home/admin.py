from django.contrib import admin
from home.models import Book,Profile,BorrowedBook,BookRequest

# Register your models here.
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BorrowedBook)
admin.site.register(BookRequest)

# by registering the model, they could be seen in the admin page
