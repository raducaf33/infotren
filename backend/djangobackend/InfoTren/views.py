from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from django.db import transaction
from  django.dispatch import receiver
from django.http import JsonResponse
import random
from django.db.models.signals import post_save

from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets
from InfoTren.serializers import UsersSerializer, RoutesSerializer, TrainsSerializer, TrainSeatsSerializer, TicketCategorySerializer, TicketsSerializer, RegisterSerializer, LoginSerializer

class FakePaymentAPIView(APIView):
    def post(self, request):
        # Preluarea detaliilor de plată din request
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')

        # Verificarea dacă toate câmpurile sunt completate
        if card_number is None or expiry_date is None or cvv is None:
            return JsonResponse({'success': False, 'message': 'Toate câmpurile sunt necesare.'}, status=400)

        # Validarea elementară a detaliilor cardului (16 cifre pentru card și 3 cifre pentru CVV)
        if len(card_number) == 16 and len(cvv) == 3:
            # Simularea unei plăți cu șanse de succes de 90%
            if random.random() < 0.9:
                return JsonResponse({'success': True, 'message': 'Plata a fost efectuată cu succes!'})
            else:
                return JsonResponse({'success': False, 'message': 'Plata a eșuat. Încercați din nou.'})
        else:
            return JsonResponse({'success': False, 'message': 'Detalii card invalide.'}, status=400)

class ConfirmBookingAPIView(APIView):
    def post(self, request):
        try:
            train_id = request.data.get('train_id')
            seat_ids = request.data.get('seat_ids')
            ticket_types = request.data.get('ticket_types')

            # Verificare dacă datele sunt valide
            if not train_id or not seat_ids or not ticket_types:
                
                return JsonResponse({'success': False, 'message': 'Missing required fields.'}, status=400)

            # Aici ar trebui să fie logica ta pentru rezervare
            # Simulează un răspuns de succes
            return JsonResponse({'success': True, 'message': 'Booking confirmed!'})
        
        except Exception as e:
            logger.error(f"Error confirming booking: {str(e)}")
            return JsonResponse({'success': False, 'message': 'A apărut o eroare. Vă rugăm să încercați din nou.'}, status=500)           

class AvailableSeatsAPIView(APIView):
    def get(self, request):
        train_id = request.query_params.get('trainId')
        if not train_id:
            return Response({"error": "Train ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        seats = TrainSeats.objects.filter(TrainId=train_id).values('SeatId', 'SeatNumber', 'Class', 'IsBooked')
        return Response(list(seats), status=status.HTTP_200_OK)

class SelectSeatAPIView(APIView):
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
                    'first_name': user.first_name,  # Include first name
                    'last_name': user.last_name
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
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
