from rest_framework import serializers
from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=('UserId','Username','Password','Firstname','Lastname','Phone','Email')

class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Routes
        fields=('RouteId','StartStation','EndStation','Distance','DepartureTime','ArrivalTime','Date')

class TrainsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trains
        fields=('TrainId','TrainNumber','Company','RouteId')

class TrainSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrainSeats
        fields=('SeatId','SeatNumber','Class','TrainId','IsBooked')

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TicketCategory
        fields=('TicketCategoryId','Type')

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tickets
        fields=('TicketId','TrainId','UserId','SeatId','TicketCategory','Price','IsPaid')


