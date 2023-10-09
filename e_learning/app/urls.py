from django.urls import path
from app.controllers.front_end import index, about,signup, contact

urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("signup/", signup, name="signup"),
    path("contact/", contact, name="contact"),
]
