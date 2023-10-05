from django.shortcuts import render
from django.http.response import HttpResponse


def index(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse("Hello, about page")
