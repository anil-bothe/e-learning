from django.shortcuts import render, redirect


def list(request):
    return render(request, 'admin/category/list.html', {})

def create(request):...
def edit(request):...
def destroy(request):...

