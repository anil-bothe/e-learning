from django.shortcuts import render
from django.http.response import HttpResponse
from app.models import Student

def index(request):
    students = Student.objects.all()
    return render(request, 'pages/index.html', {"students": students})

def about(request):
    msg = ""
    if request.method == "POST":
        data = request.POST

        obj = Student()
        obj.name = data.get("name")
        obj.dob = data.get("dob")
        obj.save()

        msg = "Successully inserted into table."

    return render(request, 'pages/about.html', {
        "name": "sursaj",
        "age": [43,22, 3],
        "msg": msg
    })


def edit(request, student_id):
    student = Student.objects.get(id=student_id)
    
    msg = ""
    if request.method == "POST":
        data = request.POST
        student.name = data.get("name")
        student.dob = data.get("dob")
        student.save()
        msg = "Successully Updated into table."

    return render(request, "pages/edit.html", {"student": student, "msg": msg})