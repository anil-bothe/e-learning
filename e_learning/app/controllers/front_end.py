from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html', {})

def course_details(request, course_id):
    return render(request, 'pages/course_details.html', {})

def about(request):
    return render(request, 'pages/about.html', {})
