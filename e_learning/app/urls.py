from django.urls import path
from app.controllers.front_end import index, about, course_details
from app.controllers.admin.assets import upload
from app.controllers.admin.dashboard import dashboard
from app.controllers.admin.course import list as courses
from app.controllers.admin.faqs import list as faqs, destroy as faqs_destroy
from app.controllers.admin.users import list as users
from app.controllers.admin.category import list as categories
from app.controllers.auth import signup, otp_verification, resend_otp, user_logout, user_login, user_profile
from uuid import uuid4


urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("course/<int:course_id>/", course_details, name="course-details"),
]

# auth
urlpatterns += [
    path("signup/", signup, name="signup"),
    path("user/login/<str:msg>/", user_login, name="user-login"),
    path("user/profile/<str:msg>/", user_profile, name="user-profile"),
    path("user/logout/", user_logout, name="user-logout"),
    path("otp/verification/<int:user_id>/", otp_verification, name="otp-verification"),
    path(f"resent/otp/{uuid4()}/<int:user_id>/", resend_otp, name="resend-otp"),
]

# backend 
urlpatterns += [
    path("user/admin/dashboard/", dashboard, name="dashboard"),
    path("user/admin/upload/file/", upload, name="upload-file"),
    path("user/admin/categories/", categories, name="category-list"),
    path("user/admin/courses/", courses, name="courses-list"),
    path("user/admin/faqs/", faqs, name="faqs-list"),
    path("user/admin/faqs/<int:faq_id>/delete/", faqs_destroy, name="faqs-destory"),
    path("user/admin/users/", users, name="users-list"),
]
