from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

'''
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
'''

class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")