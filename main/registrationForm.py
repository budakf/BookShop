from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    first_name= forms.CharField()
    last_name= forms.CharField()
    username= forms.CharField()
    email= forms.EmailField(required=True)
    password= forms.CharField(widget=forms.PasswordInput)
    re_password= forms.CharField(widget=forms.PasswordInput)