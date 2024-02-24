from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('search/', views.search_flights, name='search'),
    path('book/<int:flight_id>/', views.book_ticket, name='book_ticket'), 
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('logout/', views.logout_view, name='logout'),
]
