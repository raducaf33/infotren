from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from django.db import transaction
from  django.dispatch import receiver
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
import logging
from django.utils import timezone
from django.db.models.signals import post_save
from datetime import datetime
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets
from InfoTren.serializers import UsersSerializer, RoutesSerializer, TrainsSerializer, TrainSeatsSerializer, TicketCategorySerializer, TicketsSerializer, RegisterSerializer, LoginSerializer
class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            user.delete()  # Delete the user account
            return Response({'success': True, 'message': 'Account deleted successfully.'}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': 'Failed to delete account.'}, status=500)
class UpdateUserInformation(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'user': serializer.data}, status=200)
        return Response({'success': False, 'errors': serializer.errors}, status=400)

class UserInformation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user  # Obține utilizatorul conectat
            serializer = UsersSerializer(user)
            return Response({'success': True, 'user': serializer.data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class TicketHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user= request.user
            current_time = datetime.now()
            # Filter tickets for travel history
            history_tickets = Tickets.objects.filter(
                UserId=user,
                TrainId__RouteId__Date__lt=current_time.date()
            ) | Tickets.objects.filter(
                UserId=user,
                TrainId__RouteId__Date=current_time.date(),
                TrainId__RouteId__DepartureTime__lt=current_time.time()
            )

            # Filter tickets for active/pending trips
            active_tickets = Tickets.objects.exclude(
                TicketId__in=history_tickets.values_list('TicketId', flat=True)
            ).filter(UserId=user)

            # Serialize the data
            history_serializer = TicketsSerializer(history_tickets, many=True)
            active_serializer = TicketsSerializer(active_tickets, many=True)

            return Response({
                'success': True,
                'history': history_serializer.data,
                'active': active_serializer.data
            }, status=200)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

class TicketDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ticket_id):
        try:
            user= request.user
            ticket=Tickets.objects.get(TicketId=ticket_id, UserId=user)
            ticket.delete()
            return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

class FetchUserTickets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user= request.user
            tickets = Tickets.objects.filter(UserId=user, IsPaid=True)
            #Serialize the tickets
            serializer = TicketsSerializer(tickets, many=True)
            return Response({'success': True, 'tickets': serializer.data}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)


class FakePaymentAPIView(APIView):
    """
    Simulates a payment for unpaid tickets. 
    If payment is successful, it marks the user's unpaid tickets as paid.
    """
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can make a payment

    def post(self, request):
        # Retrieve payment details from the request
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')

        # Check if all fields are provided
        if card_number is None or expiry_date is None or cvv is None:
            return JsonResponse({'success': False, 'message': 'Toate câmpurile sunt necesare.'}, status=400)

        # Basic validation for card details (16 digits for card number and 3 digits for CVV)
        if len(card_number) == 16 and len(cvv) == 3:
            # Simulate payment with a 90% success rate
            if random.random() < 0.9:  
                # Retrieve the logged-in user
                user = request.user
                
                # Fetch all unpaid tickets for the user
                tickets = Tickets.objects.filter(UserId=user, IsPaid=False)
                
                if not tickets.exists():
                    return JsonResponse({'success': False, 'message': 'Nu există bilete neplătite pentru acest utilizator.'}, status=400)

                # Update the IsPaid status to True for all unpaid tickets
                tickets.update(IsPaid=True)

                return JsonResponse({'success': True, 'message': 'Plata a fost efectuată cu succes! Biletele dumneavoastră au fost plătite.'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Plata a esuat. Incercati din nou.'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Detalii card invalide.'}, status=400)


class ConfirmBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_price(self, train_id, seat_class, ticket_type, km):
        """Calculate the price based on distance, class, and ticket type."""
        base_price_per_km = 5  # Base price in units per km

        # Apply class multiplier
        if seat_class == 1:
            class_multiplier = 1.5
        elif seat_class == 2:
            class_multiplier = 1.2
        else:
            class_multiplier = 1.0  # Default for other classes

        # Ticket type discounts
        if ticket_type == 'Adult':
            ticket_multiplier = 1.0
        elif ticket_type == 'Student':
            ticket_multiplier = 0.7  # 30% discount for Students
        elif ticket_type == 'Pupil':
            ticket_multiplier = 0.5  # 50% discount for Pupils
        elif ticket_type == 'Senior':
            ticket_multiplier = 0.8  # 20% discount for Seniors
        else:
            ticket_multiplier = 1.0  # Default for unknown ticket types

        # Calculate the price
        price = base_price_per_km * km * class_multiplier * ticket_multiplier
        return price

    def post(self, request):
        try:
            # Log the request data
            print("Received request at /confirm-booking/")
            print("Request data:", request.data)
            print("User:", request.user)
            print("User authenticated:", request.user.is_authenticated)

            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'User is not authenticated.'}, status=401)

            train_id = request.data.get('train_id')
            seat_ids = request.data.get('seat_ids')
            ticket_types = request.data.get('ticket_types')

            if not train_id or not seat_ids or not ticket_types:
                return JsonResponse({'success': False, 'message': 'Missing required fields.'}, status=400)

            # Validate data types
            if not isinstance(seat_ids, list) or not isinstance(ticket_types, dict):
                return JsonResponse({'success': False, 'message': 'Invalid data format.'}, status=400)

            # Retrieve train and user
            train = Trains.objects.get(pk=train_id)
            user = request.user

            # Accessing the RouteId from the related Routes model
            route = train.RouteId  # Correct way to get the route information

            # Assuming that the route has a `Distance` field that gives us the km distance
            km = route.Distance  # Now we can access the distance

            booked_seats = []
            for seat_id in seat_ids:
                seat = TrainSeats.objects.get(pk=seat_id)
                if seat.IsBooked:
                    return JsonResponse({'success': False, 'message': f'Seat {seat.SeatNumber} is already booked.'}, status=400)
                booked_seats.append(seat)

            tickets = []
            for seat in booked_seats:
                for ticket_type_name, count in ticket_types.items():
                    ticket_category = TicketCategory.objects.get(Type=ticket_type_name)
                    for _ in range(count):
                        # Calculate the price dynamically
                        price = self.calculate_price(train_id, seat.Class, ticket_type_name, km)

                        ticket = Tickets(
                            TrainId=train,
                            UserId=user,
                            SeatId=seat,
                            TicketCategory=ticket_category,
                            Price=price,  # Use the calculated price here
                            IsPaid=False,
                            BookingTime=timezone.now()
                        )
                        tickets.append(ticket)

            Tickets.objects.bulk_create(tickets)

            # Mark seats as booked in bulk
            for seat in booked_seats:
                seat.IsBooked = True
            TrainSeats.objects.bulk_update(booked_seats, ['IsBooked'])

            return JsonResponse({'success': True, 'message': 'Booking confirmed!'}, status=200)

        except ObjectDoesNotExist as e:
            # Handle specific missing model errors
            return JsonResponse({'success': False, 'message': f'{str(e)} not found.'}, status=404)
        except Exception as e:
            print("Booking error:", str(e))  # Debugging
            return JsonResponse({'success': False, 'message': 'An error occurred while confirming the booking.', 'error': str(e)}, status=500)


class AvailableSeatsAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        train_id = request.query_params.get('trainId')
        if not train_id:
            return Response({"error": "Train ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        seats = TrainSeats.objects.filter(TrainId=train_id).values('SeatId', 'SeatNumber', 'Class', 'IsBooked')
        return Response(list(seats), status=status.HTTP_200_OK)

class SelectSeatAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        train_id = request.data.get('train_id')
        seat_numbers = request.data.get('seat_numbers')
        ticket_types = request.data.get('ticket_types')

        # Initialize a list to keep track of any errors
        errors = []

        # Fetch all seat instances in a single query
        seats = TrainSeats.objects.filter(SeatNumber__in=seat_numbers, TrainId=train_id)

        # Check if the number of seats fetched matches the seat_numbers provided
        if len(seats) != len(seat_numbers):
            return Response({"error": "Some seats do not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Iterate through the fetched seats and book them if available
                for seat in seats:
                    if seat.IsBooked:
                        errors.append(f"Seat {seat.SeatNumber} is already booked.")
                    else:
                        seat.IsBooked = True
                        seat.save()

            # If any errors occurred, return them in the response
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Seats booked successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here. definesc API
class SearchTicketsAPIView(APIView):
    permission_classes = [AllowAny]  # Ensure only logged-in users can confirm bookings
    def post(self, request):
        departure_place = request.data.get('departure_place')
        arrival_place = request.data.get('arrival_place')
        date = request.data.get('date')

        try:
            # Perform the search query
            routes = Routes.objects.filter(
                StartStation__icontains=departure_place,
                EndStation__icontains=arrival_place,
                Date=date
            ) 

            if routes.exists():
                route_data = []
                for route in routes:
                    # Get trains for this specific route
                    trains = Trains.objects.filter(RouteId=route)
                    route_info = {
                        'route': RoutesSerializer(route).data,
                        'trains': TrainsSerializer(trains, many=True).data,
                    }
                    route_data.append(route_info)
                    
                return Response(route_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No routes found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log the exception and return a 500 error if needed
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = Users.objects.get(email=email) 
            except Users.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',  # Add success message
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'is_admin': user.is_admin,  # Informația despre rolul utilizatorului
                    'first_name': user.first_name,  # Include first name
                    'last_name': user.last_name
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_username(request):
    username = request.GET.get('username', '')
    if User.objects.filter(username=username).exists():
        return Response({'taken': True})
    return Response({'taken': False})


def check_email(request):
    email = request.GET.get('email', '')
    if User.objects.filter(email=email).exists():
        return Response({'taken': True})
    return Response({'taken': False})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            users = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            # Debug: Print validation errors
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        

@csrf_exempt
def usersApi(request, id=0):
    if request.method=='GET':
        users = Users.objects.all()
        users_serializer= UsersSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
    elif request.method=='POST':
        users_data=JSONParser().parse(request)
        users_serializer=UsersSerializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        users_data=JSONParser().parse(request)
        users=Users.objects.get(UserId=users_data['UserId'])
        users_serializer=UsersSerializer(users, data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        users=Users.objects.get(UserId=id)
        users.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def routesApi(request, id=0):
    if request.method=='GET':
        routes = Routes.objects.all()
        routes_serializer= RoutesSerializer(routes, many=True)
        return JsonResponse(routes_serializer.data, safe=False)
    elif request.method=='POST':
        routes_data=JSONParser().parse(request)
        routes_serializer=RoutesSerializer(data=routes_data)
        if routes_serializer.is_valid():
            routes_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        routes_data=JSONParser().parse(request)
        routes=Routes.objects.get(RouteId=routes_data['RouteId'])
        routes_serializer=RoutesSerializer(routes, data=routes_data)
        if routes_serializer.is_valid():
            routes_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        routes=Routes.objects.get(RouteId=id)
        routes.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def trainsApi(request, id=0):
    if request.method=='GET':
        trains = Trains.objects.all()
        trains_serializer= TrainsSerializer(trains, many=True)
        return JsonResponse(trains_serializer.data, safe=False)
    elif request.method=='POST':
        trains_data=JSONParser().parse(request)
        trains_serializer=TrainsSerializer(data=trains_data)
        if trains_serializer.is_valid():
            trains_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        trains_data=JSONParser().parse(request)
        trains=Trains.objects.get(TrainId=trains_data['TrainId'])
        trains_serializer=TrainsSerializer(trains, data=trains_data)
        if trains_serializer.is_valid():
            trains_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        trains=Trains.objects.get(TrainId=id)
        trains.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def trainSeatsApi(request, id=0):
    if request.method=='GET':
        trainSeats = TrainSeats.objects.all()
        trainSeats_serializer= TrainSeatsSerializer(trainSeats, many=True)
        return JsonResponse(trainSeats_serializer.data, safe=False)
    elif request.method=='POST':
        trainSeats_data=JSONParser().parse(request)
        trainSeats_serializer=TrainSeatsSerializer(data=trainSeats_data)
        if trainSeats_serializer.is_valid():
            trainSeats_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        trainSeats_data=JSONParser().parse(request)
        trainSeats=TrainSeats.objects.get(TrainId=trainSeats_data['TrainId'])
        trainSeats_serializer=TrainSeatsSerializer(trains, data=trainSeats_data)
        if trainSeats_serializer.is_valid():
            trainSeats_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        trainSeats=TrainSeats.objects.get(TrainId=id)
        trainSeats.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def ticketCategoryApi(request, id=0):
    if request.method=='GET':
        ticketCategory = TicketCategory.objects.all()
        ticketCategory_serializer= TicketCategorySerializer(ticketCategory, many=True)
        return JsonResponse(ticketCategory_serializer.data, safe=False)
    elif request.method=='POST':
        ticketCategory_data=JSONParser().parse(request)
        ticketCategory_serializer=TicketCategorySerializer(data=ticketCategory_data)
        if ticketCategory_serializer.is_valid():
            ticketCategory_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        ticketCategory_data=JSONParser().parse(request)
        ticketCategory=TicketCategory.objects.get(TicketCategoryId=ticketCategory_data['TicketCategoryId'])
        ticketCategory_serializer=TicketCategorySerializer(ticketCategory, data=ticketCategory_data)
        if ticketCategory_serializer.is_valid():
            ticketCategory_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        ticketCategory=TicketCategory.objects.get(TicketCategoryId=id)
        ticketCategory.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def ticketsApi(request, id=0):
    if request.method=='GET':
        tickets = Tickets.objects.all()
        tickets_serializer= TicketsSerializer(tickets, many=True)
        return JsonResponse(ticktes_serializer.data, safe=False)
    elif request.method=='POST':
        tickets_data=JSONParser().parse(request)
        tickets_serializer=TicketsSerializer(data=tickets_data)
        if tickets_serializer.is_valid():
            tickets_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method =='PUT':
        tickets_data=JSONParser().parse(request)
        tickets=Tickets.objects.get(TicketId=tickets_data['TicketId'])
        tickets_serializer=TicketsSerializer(tickets, data=tickets_data)
        if tickets_serializer.is_valid():
            tickets_serializer.save()
            return JsonResponse("Update Succesfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        tickets=Tickets.objects.get(TicketId=id)
        tickets.delete()
        return JsonResponse("Deleted Succesfully", safe=False) 
