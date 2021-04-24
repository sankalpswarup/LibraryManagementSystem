from django.contrib import admin
from home.models import Book,Profile,BorrowedBook,BookRequest,system_variable_values

# Register your models here.
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BorrowedBook)
admin.site.register(BookRequest)
admin.site.register(system_variable_values)

# by registering the model, they could be seen in the admin page
