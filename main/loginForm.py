from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput)