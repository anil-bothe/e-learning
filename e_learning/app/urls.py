from django.urls import path
from app.controllers.front_end import index, about, edit

urlpatterns = [
    path("", index),
    path("edit/<int:student_id>/", edit),
    path("about/", about)
]
