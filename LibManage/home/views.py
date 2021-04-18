from django.shortcuts import render,HttpResponse
from home.models import Book
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Book

# Create your views here.
def index(request):
    allBooks=Book.objects.all()
    context = {
        'allBooks':allBooks
    }
    return render(request, 'index.html', context)


def bookpage(request):
    if request.method == 'POST':
        obj=Book.objects.get(id=request.POST.get('id'))
        context = {
            'title':obj.title,
            'author':obj.author,
            'publication':obj.publication,
            'genre':obj.genre,
            'summary':obj.summary,
            'available':obj.available,
        }
        return render(request, 'bookpage.html', context)

def profile(request):
    userData = User.objects.filter(name__contains='Terry')
    context = {
    "user": userData
}
    return render(request, 'profile.html',context)

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

def register(request):
    if(request.method=='POST'):
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get('email')
        user = User.objects.create_user(username,password)
        user.username=username
        user.password=password
        user.email=email
        user.save()
        return render(request, 'profile.html')
    else:
        return render(request, 'register.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return render(request, 'profile.html')

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
    return render(request, 'login.html')