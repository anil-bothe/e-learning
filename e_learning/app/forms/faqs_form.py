from django import forms

class FAQForm(forms.Form):
    question = forms.CharField(max_length=50)
    answer = forms.CharField(max_length=255)
