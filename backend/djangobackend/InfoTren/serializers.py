from rest_framework import serializers
from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = Users.objects.get(Username=username)
            except Users.DoesNotExist:
                raise serializers.ValidationError("User does not exist")

            if not check_password(password, user.Password):
                raise serializers.ValidationError("Incorrect password")
        else:
            raise serializers.ValidationError("Must include both username and password")

        data['user'] = user
        return data
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=('UserId','Username','Password','Firstname','Lastname','Phone','Email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('Username', 'password', 'confirm_password', 'Firstname', 'Lastname', 'Phone', 'Email')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        user = Users(
            Username=validated_data['Username'],
            Password=make_password(validated_data['password']),  # Hash the password
            Firstname=validated_data['Firstname'],
            Lastname=validated_data['Lastname'],
            Phone=validated_data['Phone'],
            Email=validated_data['Email']
        )
        user.save()
        return user   

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


