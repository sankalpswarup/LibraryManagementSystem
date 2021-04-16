from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("this is homepage")

def login(request):
    return HttpResponse("this is login page")

def book(request):
    return HttpResponse("this is book page")

def profile(request):
    return HttpResponse("this is profile page")