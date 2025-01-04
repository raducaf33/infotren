from django.contrib import admin
from .models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets

# Register your models here.

admin.site.register(Users)
admin.site.register(Routes)
admin.site.register(Trains)
admin.site.register(TrainSeats)
admin.site.register(TicketCategory)
admin.site.register(Tickets)
