from rest_framework import serializers
from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except ObjectDoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Use `email` instead of `username` in the authentication process
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Must include both email and password")

        data['user'] = user
        return data
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('UserId', 'first_name', 'last_name', 'email', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('password', 'confirm_password','first_name','last_name','email','phone')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        user = Users(
            password=make_password(validated_data['password']),  # Hash the password
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone']
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


