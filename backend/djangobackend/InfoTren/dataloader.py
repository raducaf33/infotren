from InfoTren.models import Routes, Trains
from datetime import date, time

route = Routes.objects.create(
    StartStation='Brasov',
    EndStation='Campina',
    Distance=74,
    DepartureTime=datetime(2024, 8, 20, 9, 0),  # Example departure time
    ArrivalTime=datetime(2024, 8, 20, 10, 30),    # Example arrival time
    Date=datetime(2024, 8, 20).date() 
)

train = Trains.objects.create(
    TrainNumber='IR345',
    Company='CFR',
    RouteId=route
)
from InfoTren.models import Routes
from datetime import date, time
route = Routes.objects.create(
    StartStation='Brasov',
    EndStatin='Bucuresti',
    Distance=166,
    DepartureTime=time(14, 0),  # Example departure time
    ArrivalTime=time(16, 30),    # Example arrival time
    Date=datetime(2024, 8, 19).date() 
)
route.save()

# Verify the data was inserted
Routes.objects.all() 