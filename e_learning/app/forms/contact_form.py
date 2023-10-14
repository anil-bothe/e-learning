from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    message = forms.CharField(max_length=255)
    email = forms.EmailField()

    # def clean_message(self):
    #     pass 
    
    # def clean_email(self):
    #     self.clearn
