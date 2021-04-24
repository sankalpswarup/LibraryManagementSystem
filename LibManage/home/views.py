from django.shortcuts import render,HttpResponse
from home.models import Book
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Book, BookRequest, BorrowedBook, system_variable_values
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, PenaltyForm
from datetime import datetime,timedelta,date


# renders the homepage of the website
def homepage(request):
    return render(request,'index.html')

# this renders the profile page of a user
def profile(request): 
    if request.user.is_authenticated:# check if the user has logged in
        context={
            'penalty1':system_variable_values.objects.all()[0].book_lost_penalty_amount,
            'penalty2':system_variable_values.objects.all()[0].issue_period_expired_penalty
        }
        return render(request, 'profile.html',context)
    else:
        return redirect('login_user')#if user is not logged in then webpage to login is opened

# renders the log page of the user/librarian/admin
def log(request):
    if request.user.is_authenticated:
        # if the user has logged in
        if request.user.profile.account_type=='user':
            # if the account from which request has come is of a 'user'
            # fetching the pending requests and borrowed books of the user and rendering them
            book_requests = BookRequest.objects.filter(user=request.user.username)
            borrowed_books = BorrowedBook.objects.filter(user=request.user.username)
            context = {
                'book_requests':book_requests,
                'borrowed_books':borrowed_books,
            }
            return render(request, 'log.html',context)
        else:
            # if the account from which request has come is of a librarian or admin
            # fetching all book requests and books borrowed and rendering them
            book_requests = BookRequest.objects.all()
            borrowed_books = BorrowedBook.objects.all()
            context = {
                'book_requests':book_requests,
                'borrowed_books':borrowed_books,
            }
            return render(request, 'log.html', context)
    else:
        # if user has not logged in
        messages.success(request, 'You must be logged in to view this page')
        return redirect('login_user')

# renders the registration page / validates the registration
def register(request):   
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('profile')
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                # if username does not exist already in database
                user = form.save()
                user.profile.account_type = 'user'
                login(request, user)
                messages.success(request, 'Account created Successfully')
                return redirect('profile')
            else:
                # if username already exits in database, or, incorrect password entered for confirmation
                messages.success(request, 'Username already exists, or confirmation password incorrect')
                return redirect('register')

        # if request is for rendering the registration form
        return render(
                request, "register.html",
                {"form": CustomUserCreationForm}
            )

# called when admin or librarian wants to see/find users registered in the system
def display_users(request):
    if(request.user.is_authenticated):
        if(request.user.profile.account_type!='user'):
            # account with 'user' priveleges can't view these details
            if request.method=='POST':
                # if a username is searched
                uname=request.POST.get('uname')
                allusers=User.objects.filter(username__contains=uname)
            else:
                # if request has come to display all users
                allusers=User.objects.all()
            # penalty form is used by librarian/admin to update a users due penalty 
            form = PenaltyForm()
            context = {
                'penalty_form':form,
                'user_set':allusers
            }
            return render(request,'users.html',context)

# authenticates user details / renders the login page
def loginUser(request):
    if request.user.is_authenticated:
        # if person is already logged in
        return redirect('profile')
    else:
        if request.method=="POST":
            # if user has filled the login details and submitted
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # check if user has entered correct credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                # Valid credentials entered
                login(request, user) # login the user
                messages.success(request, 'Successfully Logged In')
                return redirect('profile')
            else:
                # Invalid credentials entered
                messages.success(request, 'Invalid Username or Password')
                return render(request, 'login.html')
        
        # if request has come to display the login page
        return render(request, 'login.html')

# loggin user out
def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login_user')

# called when admin wants to make a 'user' librarian or vice versa
def change_account_type(request):
    if request.method=='POST':
        user_id=request.POST.get('id')
        # updating the account type of the account
        new_account_type=request.POST.get('account_type')
        user_object=User.objects.get(id=user_id)
        user_object.profile.account_type=new_account_type
        user_object.profile.save()
        # redirecting to dispaly all accounts
        return redirect('display_users')

# called to update the penalty amount of a user
def penalty_returned(request):
    if request.method == 'POST':
        # if form is submitted with the penalty amount submitted data
        # creating a form instance and populating it with data from the request:
        form = PenaltyForm(request.POST)
        # checking whether it's valid:
        if form.is_valid():
            # processing the data in form.cleaned_data
            amount_given = form.cleaned_data['penalty_amount']
            user_object=User.objects.get(id=request.POST.get('id'))
            old_penalty=user_object.profile.penalty
            new_penalty=old_penalty-amount_given
            user_object.profile.penalty=new_penalty
            user_object.profile.save()
            # redirecting to display all accounts
            return redirect("display_users")

# renders the page to add a book in database
def addBook(request):
    if(request.user.is_authenticated):
        if(request.user.profile.account_type!='user'):
            # if request has come from an account of librarian or admin
            if request.method == 'POST':
                # getting the book details from the form
                title = request.POST.get('title')
                ISBN = request.POST.get('ISBN')
                author = request.POST.get('author')
                publication = request.POST.get('publication')
                genre = request.POST.get('genre')
                qty = request.POST.get('quantity')
                qty=int(qty)
                summary = request.POST.get('summary')
                # checking if the book already exits in database
                old_item=Book.objects.filter(title=title,ISBN=ISBN,author=author,publication=publication,genre=genre)
                if old_item.exists():
                    # if the book which is being added already exixts in the databse
                    book=old_item[0]
                    messages.success(request, 'Book already exists in database')
                else:
                    # if the book being added does not exist in the databse
                    # creating a new book object and saving it in database
                    book=Book(title=title,ISBN=ISBN,author=author,publication=publication,genre=genre,available='Available',summary=summary,quantity=qty)
                    book.save()
                    messages.success(request, 'A new book has been added!')

                # endering the details page of the book which already existed, or of the new book added
                context = {
                    'title':book.title,
                    'author':book.author,
                    'publication':book.publication,
                    'isbn':book.ISBN,
                    'genre':book.genre,
                    'summary':book.summary,
                    'available':book.available,
                    'id':book.id,
                    'quantity':book.quantity

                }
                return render(request, 'bookpage.html',context)
            
            # if the call to this function came from a link which is to open the add book page, the add book page is rendered
            return render(request,'addbook.html')
        else:
            # if request to open this page came from an account which is of a 'user'
            messages.success(request, 'This page can be accessed only by librarians or admins')
            return redirect('profile')

    else:
        # if request to open this page came when no the person has not logged in
        messages.success(request, 'Please login first')
        return redirect('login_user')

# renders edit book details form
def edit_book(request):
    if(request.user.is_authenticated):
        if(request.user.profile.account_type!='user'):
            if request.method=='GET':
                # the databse id of book which has to be edited is present in the http request sent by form
                obj=Book.objects.get(id=request.GET.get('id'))
                # rendering the edit details page
                context = {
                    'title':obj.title,
                    'isbn':obj.ISBN,
                    'author':obj.author,
                    'publication':obj.publication,
                    'genre':obj.genre,
                    'summary':obj.summary,
                    'quantity':obj.quantity,
                    'id':obj.id,
                    }
                return render(request, 'editBook.html',context)

# updates the database when update book details form is submitted
def book_edited(request):
    if request.method == 'POST':
        # fetching the book object whose details are being updated
        obj=Book.objects.get(id=request.POST.get('id'))
        # updating the details
        obj.title = request.POST.get('title')
        obj.ISBN = request.POST.get('ISBN')
        obj.author = request.POST.get('author')
        obj.publication = request.POST.get('publication')
        obj.genre = request.POST.get('genre')
        obj.quantity = int(request.POST.get('quantity'))
        obj.summary = request.POST.get('summary')
        # saving the object after updating
        obj.save()
        # rendering the book details page with updated details
        messages.success(request, 'Book Details has been updated!')
        context = {
            'title':obj.title,
            'author':obj.author,
            'publication':obj.publication,
            'isbn':obj.ISBN,
            'genre':obj.genre,
            'summary':obj.summary,
            'available':obj.available,
            'id':obj.id,
            'quantity':obj.quantity,
        }
        return render(request, 'bookpage.html', context)

# called when a book is to be deleted from database
def delete_book(request):
    if request.method=='POST':
        # fetching the book object to be deleted
        book_object=Book.objects.get(id=request.POST.get('id'))
        # verifying the librarian/admin password as a security measure before deleting a book
        password = request.POST.get('password')
        username=request.user.username
        user_check = authenticate(username=username, password=password)
        if user_check is not None:
            # if correct password is entered, deleting the book
            book_object.delete()
            messages.success(request, 'Book deleted Successfully')
            return render(request,'index.html')
        else:
            # if incorrect password is entered, rendering the book details page of that book again
            context = {
                'title':book_object.title,
                'author':book_object.author,
                'publication':book_object.publication,
                'isbn':book_object.ISBN,
                'genre':book_object.genre,
                'summary':book_object.summary,
                'available':book_object.available,
                'id':book_object.id,
                'quantity':book_object.quantity,
            }
            messages.success(request, 'Wrong Password Entered')
            return render(request, 'bookpage.html', context) #details page of that book is rendered

# this renders the page displaying all books in the library
def all_books(request): 
    allBooks=Book.objects.all() #fetching all books in database
    context = {
        'allBooks':allBooks
    }
    return render(request, 'all_books.html', context) #rendering page displaying all books

# called when books are searched by title, author or genre
def book_searched(request):
    if request.method=='GET':
        if(request.GET.get('type')=='title'):
            # books searched by title
            q=request.GET.get('q')
            obj=Book.objects.filter(title__icontains=q)
        elif request.GET.get('type')=='author':
            # books searched by author
            q=request.GET.get('q')
            obj=Book.objects.filter(author__icontains=q)
        elif request.GET.get('type')=='genre' :
            # books searched by genre
            genre_selected=request.GET.get('genre')
            obj=Book.objects.filter(genre=genre_selected)
        # rendering the page with searched results
        context = {
            'books':obj,
        }
        return render(request,'filtered_books.html',context)

#this renders the details page of a book
def bookpage(request):
    # this function is called when button to view a book details is pressed, which sends a form having the database id of that book

    if request.method == 'GET': # performing this check as a precautionry measure to avoid erros on website
        obj=Book.objects.get(id=request.GET.get('id'))

        is_borrowed=BorrowedBook.objects.filter(title=obj.title,user=request.user,author=obj.author,ISBN=obj.ISBN)

        context = {
            'title':obj.title,
            'author':obj.author,
            'publication':obj.publication,
            'isbn':obj.ISBN,
            'genre':obj.genre,
            'summary':obj.summary,
            'available':obj.available,
            'id':obj.id,
            'is_borrowed':is_borrowed,
            'quantity':obj.quantity
        }
        return render(request, 'bookpage.html', context) #details page of that book is rendered

#this function is called when a logged in user gives a request to borrow a book
def borrow_book(request): 

    if request.method=='POST': # precautionary measure
        bookitem=Book.objects.get(id=request.POST.get('id'))

        # converting period of issue from string to integer
        str2num = { "7":7, "2":2, "5":5, "10":10, "14":14}
        pd=str2num[request.POST.get('period')]

        # creating a new request object in database
        request_item=BookRequest(user=request.user.username,ISBN=bookitem.ISBN,title=bookitem.title,author=bookitem.author,period=pd)
        request_item.save()

        messages.success(request, 'Your request has been registered')
        return redirect('log')
    return redirect('profile')

# when librarian/admin accepts a user's request to borrow/renew a book
def request_accepted(request):
    if request.user.is_authenticated:# check if the user has logged in
        if request.user.profile.account_type!='user':# check if the user is 'librarian' / 'admin'
            if request.method=='POST': # librarian accepted the request

                # getting details of the request from database
                request_item =BookRequest.objects.get(id=request.POST.get('id'))
                
                # evaluating date of issue, and due date to return
                pd=request_item.period
                date=datetime.today()
                date2=datetime.now() + timedelta(days = pd)
                date3=date2.date()

                # finding if the book requested is already borrowed by same user, in which case user must have requested to renew the period of issue
                is_renew=False
                old_item=BorrowedBook.objects.filter(user=request_item.user,ISBN=request_item.ISBN,title=request_item.title,author=request_item.author)
                if old_item.exists():
                    is_renew=True
                    old_item.delete() # deleting the old object of borrowed book, if request is to renew the period of issue of book

                # creating a new borrowed book object in database
                borrowed_item=BorrowedBook(user=request_item.user,ISBN=request_item.ISBN,title=request_item.title,author=request_item.author,date=date,period=pd,due_date=date3)
                borrowed_item.save()

                # decreasing no. of those books in library by 1
                book_item=Book.objects.get(ISBN=request_item.ISBN,title=request_item.title,author=request_item.author)
                if not is_renew:
                    # if user is not renewing the book, then only quantity to be changed
                    qty = book_item.quantity
                    book_item.quantity=qty-1
                book_item.save()
                # deleting the request object from database
                request_item.delete()

                return redirect('log')
    return redirect('profile')

# librarian/admin has rejected a request to borrow/renew a book
def request_rejected(request):
    if request.user.is_authenticated:# check if the user has logged in
        if request.user.profile.account_type!='user':# check if the user is 'librarian' or  'admin'
            if request.method=='POST': 
                # finding the request object and deleting it
                request_item =BookRequest.objects.get(id=request.POST.get('id'))
                request_item.delete()
                return redirect('log')
    return redirect('profile')

# when librarian wants to issue\renew a book
def issue_book(request):
    if request.user.is_authenticated:# check if the user has logged in
        if request.user.profile.account_type!='user':# check if the user is 'librarian' or  'admin'
            if request.method=='POST': 
                user_item=User.objects.filter(username=request.POST.get('user'))
                if user_item:
                    str2num = { "7":7, "2":2, "5":5, "10":10, "14":14}
                    pd=str2num[request.POST.get('period')]
                    is_renew=False
                    date=datetime.today()
                    date2=datetime.now() + timedelta(days = pd)
                    date3=date2.date()
                    book_item=Book.objects.get(id=request.POST.get('id'))
                    # finding if the book requested is already borrowed by same user, in which case user must have requested to renew the period of issue
                    old_item=BorrowedBook.objects.filter(user=request.POST.get('user'),ISBN=book_item.ISBN,title=book_item.title,author=book_item.author)
                    if old_item.exists():
                        is_renew=True
                        old_item.delete() # deleting the old object of borrowed book, if request is to renew the period of issue of book

                    # creating a new borrowed book object in database
                    borrowed_item=BorrowedBook(user=request.POST.get('user'),ISBN=book_item.ISBN,title=book_item.title,author=book_item.author,date=date,period=pd,due_date=date3)
                    borrowed_item.save()

                    # decreasing no. of those books in library by 1
                    book_item=Book.objects.get(ISBN=book_item.ISBN,title=book_item.title,author=book_item.author)
                    if not is_renew:
                        # if user is not renewing the book, then only quantity to be changed
                        qty = book_item.quantity
                        book_item.quantity=qty-1
                    book_item.save()
                    messages.success(request, 'Book Issued')
                    return redirect('all_books')
                else:
                    messages.success(request, 'Invalid Username entered')
                    return redirect('all_books')
                
# when user has returned the book to library, and librarian/admin wants to update the database
def book_returned(request): 
    if request.user.is_authenticated:# check if the user has logged in
        if request.user.profile.account_type!='user':# check if the user is 'librarian' or  'admin'
            if request.method=='POST': # book returned
                borrowed_item =BorrowedBook.objects.get(id=request.POST.get('id'))
                user_item_name=borrowed_item.user
                borrowed_item.delete() # deleting the borrowed book entry from database
                # increasing no. of those books in library by 1
                book_item=Book.objects.get(ISBN=borrowed_item.ISBN,title=borrowed_item.title,author=borrowed_item.author)
                qty = book_item.quantity
                book_item.quantity=qty+1
                book_item.save()

                d0=borrowed_item.due_date
                year=int(d0.strftime("%Y"))
                month=int(d0.strftime("%m"))
                day=int(d0.strftime("%d"))
                due_date = date(year, month, day)
                return_date=date.today()            
                if(return_date > due_date):
                    num_days=(return_date-due_date).days
                    penalty=num_days*system_variable_values.objects.all()[0].issue_period_expired_penalty
                    user_item=User.objects.filter(username=user_item_name)[0]
                    old_penalty=user_item.profile.penalty
                    new_penalty=old_penalty+penalty
                    user_item.profile.penalty=new_penalty
                    user_item.profile.save()

                return redirect('log')
    return redirect('profile')

# called when user wants to renew the time period for which a book is borrowed
def renew_period(request):
    if request.method=='POST':
        # fetching the borrowed book object
        borrowed_book_id=request.POST.get('id')
        borrowed_book=BorrowedBook.objects.get(id=borrowed_book_id)
        # extracting the number of days for which the period has to be renewed
        str2num = { "7":7, "2":2, "5":5, "10":10, "14":14}
        pd=str2num[request.POST.get('period')]
        # creating a new request for that book, by that user, but with a new issue period
        request_item=BookRequest(user=request.user.username,ISBN=borrowed_book.ISBN,title=borrowed_book.title,author=borrowed_book.author,period=pd)
        request_item.save()
        messages.success(request, 'Your request has been registered')
        # rendering the log page where user can see the new request
        return redirect('log')

# called when user wants to update the a borrowed book is lost
def book_lost(request):
    if request.method=='POST':
        # getting the deatils of the borrowed book
        borrowed_book_id=request.POST.get('id')
        borrowed_book=BorrowedBook.objects.get(id=borrowed_book_id)
        # deleting the book from borrowed book database
        borrowed_book.delete()
        # updating the penalty amount of the user
        old_penalty=request.user.profile.penalty
        new_penalty=old_penalty+system_variable_values.objects.all()[0].book_lost_penalty_amount
        request.user.profile.penalty=new_penalty
        request.user.profile.save()
        # rendering the profile page
        return redirect('profile')

# called when librarian/admin wants to change the penalty applied 
def update_penalty_amount(request):
    if request.user.is_authenticated:# check if the user has logged in
        if request.user.profile.account_type!='user':# check if the user is 'librarian' or  'admin'
            if request.method=='POST':
                variable=system_variable_values.objects.all()
                if variable:
                    value=request.POST.get('penalty')
                    penalty_for=request.POST.get('type')
                    if penalty_for=='book_lost':
                        variable[0].book_lost_penalty_amount=int(value)
                    else:
                        variable[0].issue_period_expired_penalty=int(value)
                    variable[0].save()
                    system_variable_values.objects.all()[0].book_lost_penalty_amount
                    system_variable_values.objects.all()[0].issue_period_expired_penalty
    return redirect('profile')
   


