from django.shortcuts import render, redirect


def list(request):
    return render(request, 'admin/courses/list.html', {})
