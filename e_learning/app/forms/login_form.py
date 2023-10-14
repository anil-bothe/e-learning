from django import forms


class LoginForm(forms.Form):
    fname = forms.CharField(max_length=10)
    lname = forms.CharField(max_length=10)
    email = forms.EmailField()
    password = forms.CharField(max_length=20)
