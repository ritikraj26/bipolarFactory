from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    airline = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.origin} to {self.destination} - {self.airline}"

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()  
    booking_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username} - Flight: {self.flight}"
