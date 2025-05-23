from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "text",
        "placeholder": " enter username", 
    }), label="Username")

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "email",
        "placeholder": " enter email ", 
    }))
    
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "password",
        "placeholder": " enter password ", 
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "password",
        "placeholder": " re-enter password ", 
    }))


    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']