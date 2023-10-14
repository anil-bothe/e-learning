from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models



class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    phone_no = models.CharField(max_length = 10)

    login_attempt = models.IntegerField(default=0)
    otp = models.CharField(max_length=6, null=True)
    blocked_datetime = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    STATUS_BY = (
        (0, "Inactive"),
        (1, "Active"),
        (2, "Blocked"),
    )
    status = models.IntegerField(choices=STATUS_BY, default=0)


    def __str__(self):
        return "{}".format(self.email)
    
