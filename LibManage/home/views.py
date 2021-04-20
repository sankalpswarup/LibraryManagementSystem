from django.shortcuts import render,HttpResponse
from home.models import Book
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Book, BookRequest, BorrowedBook
from django.shortcuts import redirect
from .forms import CustomUserCreationForm

# Create your views here.
def index(request):
    try:
        allBooks=Book.objects.all()
    except Book.DoesNotExist:
        allBooks=None

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
            'isbn':obj.ISBN,
            'genre':obj.genre,
            'summary':obj.summary,
            'available':obj.available,
            'id':obj.id,
        }
        return render(request, 'bookpage.html', context)

def profile(request):
    # check if the user has logged in
    if request.user.is_authenticated:
        if request.user.profile.account_type=='user':
            if request.method=='POST': # user has requested to borrow book
                bookitem=Book.objects.get(id=request.POST.get('id'))
                request_item=BookRequest(user=request.user.username,ISBN=bookitem.ISBN,title=bookitem.title,author=bookitem.author)
                request_item.save()
                messages.success(request, 'Your request has benn registered')
            
            try:
                book_requests = BookRequest.objects.filter(user=request.user.username)
            except BookRequest.DoesNotExist:
                book_requests = None
            try:
                borrowed_books = BorrowedBook.objects.filter(user=request.user.username)
            except BorrowedBook.DoesNotExist:
                borrowed_books = None
            context = {
                'book_requests':book_requests,
                'borrowed_books':borrowed_books,
            }
            return render(request, 'profile.html',context)
        else:
            if request.method=='POST': # librarian accepted the request
                request_item =BookRequest.objects.get(id=request.POST.get('id'))
                borrowed_item=BorrowedBook(user=request_item.user,ISBN=request_item.ISBN,title=request_item.title,author=request_item.author)
                borrowed_item.save()
                request_item.delete()
            try:
                book_requests = BookRequest.objects.all()
            except BookRequest.DoesNotExist:
                book_requests = None
            
            try:
                borrowed_books = BorrowedBook.objects.all()
            except BorrowedBook.DoesNotExist:
                borrowed_books = None
            context = {
                'book_requests':book_requests,
                'borrowed_books':borrowed_books,
            }
            return render(request, 'profile.html', context)

    else:
        return redirect('login_user')

def addBook(request):
    if(request.user.is_authenticated):
        if(request.user.profile.account_type!='user'):
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
        else:
            messages.success(request, 'This page can be accessed only by librarians')
            return redirect('profile')

    else:
        messages.success(request, 'Please login first')
        return redirect('login_user')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # check if user has entered correct credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                messages.success(request, 'Successfully Logged In')
                return redirect('profile')
            else:
                # No backend authenticated the credentials
                messages.success(request, 'Invalid Username or Password')
                return render(request, 'login.html')
        return render(request, 'login.html')


def register(request):    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.account_type = 'user'
            login(request, user)
            messages.success(request, 'Account created Successfully')
            return redirect('profile')
        else:
            messages.success(request, 'Invalid details entered')
            return redirect('register')

    return render(
            request, "register.html",
            {"form": CustomUserCreationForm}
        )

def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login_user')

def edit_book(request):
    if request.method == 'POST':
        obj=Book.objects.get(id=request.POST.get('id'))
        obj.title = request.POST.get('title')
        obj.ISBN = request.POST.get('ISBN')
        obj.author = request.POST.get('author')
        obj.publication = request.POST.get('publication')
        obj.genre = request.POST.get('genre')
        obj.available = request.POST.get('available')
        obj.summary = request.POST.get('summary')
        obj.save()
        messages.success(request, 'Book Details has been updated!')
    elif request.method=='GET':
        obj=Book.objects.get(id=request.GET.get('id'))

    context = {
        'title':obj.title,
        'isbn':obj.ISBN,
        'author':obj.author,
        'publication':obj.publication,
        'genre':obj.genre,
        'summary':obj.summary,
        'available':obj.available,
        'id':obj.id,
        }
    return render(request, 'editBook.html',context)
def change_access(request):
    request.user.profile.account_type='librarian'
    return redirect('profile')

def book_returned(request):
    if request.method=='POST': # book returned
        request_item =BorrowedBook.objects.get(id=request.POST.get('id'))
        request_item.delete()
    return redirect('profile')
