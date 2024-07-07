from django.db import models

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
    DepartureTime = models.DateTimeField()
    ArrivalTime = models.DateTimeField()
    Date = models.DateField()

class Trains(models.Model):
    TrainId = models.AutoField(primary_key=True)
    TrainNumber = models.CharField(max_length=500)
    Company = models.CharField(max_length=500)
    Distance = models.IntegerField()
    DepartureTime = models.DateTimeField()
    ArrivalTime = models.DateTimeField()
    Date = models.DateField()
    