from django.shortcuts import render, redirect
from django.http.response import JsonResponse


def upload(request):
    d = {
        "name": "vaishnavi"
    }
    return JsonResponse(d)