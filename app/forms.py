from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class UserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=14)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    position = forms.CharField(max_length=50)
    salary = forms.IntegerField()

    class Meta:
        model = models.Workers
        fields = ('username', 'email', 'password1', 'password2')


class BuyTicketForm(forms.Form):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    row = forms.IntegerField()
    seat = forms.IntegerField()


class GenreForm(forms.ModelForm):

    class Meta:
        model = models.Genres
        fields = ('name', 'description')


class MovieForm(forms.ModelForm):

    class Meta:
        model = models.Movies
        fields = '__all__'


class DiscountForm(forms.ModelForm):

    class Meta:
        model = models.Discounts
        fields = '__all__'
