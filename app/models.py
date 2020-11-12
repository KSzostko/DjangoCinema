from django.db import models
from django.contrib.auth.models import User, PermissionsMixin


class Clients(models.Model):
    phone_number = models.CharField(unique=True, max_length=14)
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
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    room = models.ForeignKey(Rooms, models.DO_NOTHING)


class Seats(models.Model):
    room = models.ForeignKey(Rooms, models.DO_NOTHING)
    nr_row = models.IntegerField()
    nr_seat = models.IntegerField()
    surname = models.CharField(max_length=50)


class Tickets(models.Model):
    seance = models.ForeignKey(Seances, models.DO_NOTHING)
    seat = models.ForeignKey(Seats, models.DO_NOTHING)
    discount = models.ForeignKey(Discounts, models.DO_NOTHING)
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    price = models.IntegerField()


class Workers(User, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=14)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    salary = models.IntegerField()
    date_of_employment = models.DateField()
    seances = models.ManyToManyField(Seances)
