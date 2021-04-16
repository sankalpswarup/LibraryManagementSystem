from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    context = {
        'variable':"this is sent"
    }
    return render(request, 'index.html', context)


def book(request):
    return render(request, 'book.html')

def profile(request):
    return render(request, 'profile.html')