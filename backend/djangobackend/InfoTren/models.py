from django.db import models
from datetime import datetime
# Create your models here.

class Users(models.Model):
    UserId = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=500)
    Password=models.CharField(max_length=500)
    Firstname = models.CharField(max_length=500)
    Lastname = models.CharField(max_length=500)
    Phone = models.CharField(max_length=10)
    Email =models.CharField(max_length=500)

class Routes(models.Model):
    RouteId = models.AutoField(primary_key=True)
    StartStation = models.CharField(max_length=500)
    EndStation = models.CharField(max_length=500)
    Distance = models.IntegerField()
    DepartureTime = models.TimeField()
    ArrivalTime = models.TimeField()
    Date = models.DateField()
  

class Trains(models.Model):
    TrainId = models.AutoField(primary_key=True)
    TrainNumber = models.CharField(max_length=500)
    Company = models.CharField(max_length=500)
    RouteId = models.ForeignKey(Routes, on_delete=models.CASCADE)
    
class TrainSeats(models.Model):
    SeatId = models.AutoField(primary_key=True)
    SeatNumber = models.IntegerField()
    Class = models.IntegerField()
    TrainId = models.ForeignKey('Trains', on_delete=models.CASCADE)
    IsBooked = models.BooleanField(default=False)

class TicketCategory(models.Model):
    TicketCategoryId = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=500)

class Tickets(models.Model):
    TicketId = models.AutoField(primary_key=True)
    TrainId = models.ForeignKey('Trains', on_delete=models.CASCADE)
    UserId = models.ForeignKey('Users', on_delete=models.CASCADE)
    SeatId = models.ForeignKey('TrainSeats', on_delete=models.CASCADE)
    TicketCategory = models.ForeignKey('TicketCategory', on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    IsPaid = models.BooleanField(default=False)

    