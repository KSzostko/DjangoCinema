from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from datetime import datetime


class Clients(models.Model):
    phone_number = models.CharField(max_length=14)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return f'Client {self.name} {self.surname}, phone: {self.phone_number}'


class Discounts(models.Model):
    name = models.CharField(unique=True, max_length=50)
    value = models.IntegerField()

    def __str__(self):
        return f'Discount {self.name} worth {self.value}'


class Genres(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'Genre {self.name} with the description: {self.description}'


class Movies(models.Model):
    title = models.CharField(unique=True, max_length=50)
    release_date = models.DateField()
    duration = models.IntegerField()
    age_restriction = models.IntegerField()
    director = models.CharField(max_length=20)
    cast = models.TextField()
    description = models.TextField()
    genres = models.ManyToManyField(Genres)

    def __str__(self):
        return f'Movie {self.title} released {self.release_date}'


class Rooms(models.Model):
    size = models.IntegerField(unique=True)

    def __str__(self):
        return f'Room number {self.id} of size {self.size}'


class Seances(models.Model):
    date = models.DateTimeField()
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)

    def __str__(self):
        return f'Seance {self.movie.title} in the room {self.room.id} on the day {self.date}'


class Seats(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    nr_row = models.IntegerField()
    nr_seat = models.IntegerField()

    def __str__(self):
        return f'Seat number {self.nr_seat} in row {self.nr_row} in the room {self.room.id}'


class Tickets(models.Model):
    seance = models.ForeignKey(Seances, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discounts, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'Ticket for the {self.seance} for {self.client}'


class Workers(User, PermissionsMixin):
    phone_number = models.CharField(max_length=14)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    salary = models.IntegerField(default=1000)
    date_of_employment = models.DateField(default=datetime.now)
    seances = models.ManyToManyField(Seances)

    def __str__(self):
        return f'Worker {self.name} {self.surname} working on the position {self.position}'
