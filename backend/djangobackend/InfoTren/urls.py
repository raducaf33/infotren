from django.urls import re_path, path
from InfoTren import views


urlpatterns=[
    re_path(r'^users$', views.usersApi),
    re_path(r'^users/([0-9]+)$', views.usersApi),

    re_path(r'^routes$', views.routesApi),
    re_path(r'^routes/([0-9]+)$', views.routesApi),

    re_path(r'^trains$', views.trainsApi),
    re_path(r'^trains/([0-9]+)$', views.trainsApi),

    re_path(r'^trainSeats$', views.trainSeatsApi),
    re_path(r'^trainSeats/([0-9]+)$', views.trainSeatsApi),

    re_path(r'^ticketCategory$', views.ticketCategoryApi),
    re_path(r'^ticketCategory/([0-9]+)$', views.ticketCategoryApi),

    re_path(r'^tickets$', views.ticketsApi),
    re_path(r'^tickets/([0-9]+)$', views.ticketsApi),

    re_path(r'^register$', views.RegisterView.as_view()), # User registration
    re_path(r'check-username/', views.check_username,),
    re_path(r'check-email/', views.check_email),
    re_path(r'^login/$', views.LoginAPIView.as_view()),

    re_path(r'^search-tickets/$', views.SearchTicketsAPIView.as_view()),

    re_path(r'^api/seats$', views.AvailableSeatsAPIView.as_view()),

    re_path(r'^confirm-booking/?$', views.ConfirmBookingAPIView.as_view()),
    re_path(r'^fake-payment/', views.FakePaymentAPIView.as_view()),
    re_path(r'^fetch-user-tickets/$', views.FetchUserTickets.as_view()),

    re_path(r'^delete-tickets/(?P<ticket_id>\d+)/$', views.TicketDelete.as_view()),

    re_path(r'^tickets-history/', views.TicketHistory.as_view()),
    re_path(r'^user-information/', views.UserInformation.as_view()),

    re_path(r'update-user-information/', views.UpdateUserInformation.as_view(), name='update-user-information'),
    re_path(r'delete-account/', views.DeleteAccount.as_view(), name='delete-account')
     
]