from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from InfoTren.models import Users, Routes, Trains, TrainSeats, TicketCategory, Tickets
from InfoTren.serializers import UsersSerializer, RoutesSerializer, TrainsSerializer, TrainSeatsSerializer, TicketCategorySerializer, TicketsSerializer

# Create your views here. definesc API

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

