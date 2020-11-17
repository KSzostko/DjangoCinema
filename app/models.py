from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from datetime import datetime


class Clients(models.Model):
    phone_number = models.CharField(max_length=14)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)


class Discounts(models.Model):
    name = models.CharField(unique=True, max_length=50)
    value = models.IntegerField()


class Genres(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=100, )


class Movies(models.Model):
    title = models.CharField(unique=True, max_length=50)
    release_date = models.DateField()
    duration = models.IntegerField()
    age_restriction = models.IntegerField()
    director = models.CharField(max_length=20)
    cast = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genres)


class Rooms(models.Model):
    size = models.IntegerField(unique=True)


class Seances(models.Model):
    date = models.DateTimeField()
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)


class Seats(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    nr_row = models.IntegerField()
    nr_seat = models.IntegerField()
    surname = models.CharField(max_length=50)


class Tickets(models.Model):
    seance = models.ForeignKey(Seances, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    price = models.IntegerField()


class Workers(User, PermissionsMixin):
    phone_number = models.CharField(max_length=14)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    salary = models.IntegerField(default=1000)
    date_of_employment = models.DateField(default=datetime.now)
    seances = models.ManyToManyField(Seances)
