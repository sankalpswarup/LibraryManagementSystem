from django.shortcuts import render,HttpResponse
from home.models import Book
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'variable':"this is sent"
    }
    return render(request, 'index.html', context)


def bookpage(request):
    return render(request, 'bookpage.html')

def profile(request):
    return render(request, 'profile.html')

def addBook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        ISBN = request.POST.get('ISBN')
        author = request.POST.get('author')
        publication = request.POST.get('publication')
        genre = request.POST.get('genre')
        available = request.POST.get('available')
        summary = request.POST.get('summary')
        book=Book(title=title,ISBN=ISBN,author=author,publication=publication,genre=genre,available=available,summary=summary)
        book.save()
        messages.success(request, 'A new book has been added!')

    return render(request, 'addBook.html')