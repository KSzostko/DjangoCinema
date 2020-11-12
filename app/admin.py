from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Genres)
admin.site.register(models.Seances)
admin.site.register(models.Workers)
admin.site.register(models.Seats)
admin.site.register(models.Rooms)
admin.site.register(models.Movies)
admin.site.register(models.Discounts)
admin.site.register(models.Tickets)
admin.site.register(models.Clients)
