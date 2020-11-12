from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Workers


class UserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=14)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    position = forms.CharField(max_length=50)
    salary = forms.IntegerField()

    class Meta:
        model = Workers
        fields = ('username', 'email', 'password1', 'password2')