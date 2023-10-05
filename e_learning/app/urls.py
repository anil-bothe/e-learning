from django.urls import path
from app.controllers.front_end import index, about

urlpatterns = [
    path("", index),
    path("about/", about)
]
