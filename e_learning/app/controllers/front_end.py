from django.shortcuts import render
from django.http.response import HttpResponse


def index(request):
    return render(request, 'pages/index.html', {})

def contact(request):
    return render(request, 'pages/contact.html', {})

def about(request):
    return render(request, 'pages/about.html', {})

def signup(request):
    return render(request, 'pages/signup.html', {})


# - -------------- extra functions --------------- #
