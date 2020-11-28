from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models

#link z którego korzystałem
#https://stackoverflow.com/questions/14660037/django-forms-pass-parameter-to-form

class UserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=14)
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    position = forms.CharField(max_length=50)
    salary = forms.IntegerField()

    class Meta:
        model = models.Workers
        fields = ('username', 'email', 'password1', 'password2')

''' ORGINAŁ
class BuyTicketForm(forms.Form):    
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    row = forms.IntegerField()
    seat = forms.IntegerField()

''' 
class BuyTicketForm(forms.Form):
    '''
    def __init__(self,*args,**kwargs):
        super(BuyTicketForm,self).__init__(*args,**kwargs)
        self.discnt = args[0]['discnt'] 
        self.fields['discount'].widget = forms.Select(choices=tuple([(name, name) for name in self.discnt])) 
        '''
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    row = forms.IntegerField()
    seat = forms.IntegerField()
    #test
    #discount = forms.CharField(max_length = 50)


class DeleteTicketForm(forms.Form):
    ticket_number = forms.IntegerField()
    phone_number = forms.CharField(max_length=14)


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


class RoomForm(forms.ModelForm):

    class Meta:
        model = models.Rooms
        fields = '__all__'


class SeatForm(forms.ModelForm):

    class Meta:
        model = models.Seats
        fields = '__all__'


class SeanceForm(forms.ModelForm):

    class Meta:
        model = models.Seances
        fields = '__all__'
