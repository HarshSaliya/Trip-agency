from django.db import models
from django import forms
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User


from django.utils import timezone



class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=2)

    def __str__(self):
        return self.country
    


class Detailed_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=20)
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.IntegerField(default=5)
    dest_name = models.CharField(max_length=25 ,  unique=True)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()

    def __str__(self):
        return self.dest_name
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class DayDescription(models.Model):
    detailed_desc = models.ForeignKey(Detailed_desc, related_name='day_descriptions', on_delete=models.CASCADE)
    day_number = models.IntegerField() 
    description = models.CharField(max_length=200) 


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    destination = models.ForeignKey(Detailed_desc,to_field='dest_name' , on_delete=models.CASCADE, related_name='trips')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trips')
    trip_date = models.DateField()

    def __str__(self):
        return  f"{self.destination} - {self.city} -{self.trip_date}"


@property
def destination_name(self):
        # This will allow you to access dest_name directly as a property
        return self.destination.dest_name

def __str__(self):
        return f"Trip to {self.destination_name} from {self.city.name} on {self.trip_date}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who owns the wishlist
    destination = models.ForeignKey(Detailed_desc, on_delete=models.CASCADE)  # Destination in wishlist
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp for when added

    def __str__(self):
        return f"{self.user.username} - {self.destination.country}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    number_of_passengers = models.IntegerField(default=1, null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, 
        default='pending', 
        choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failure', 'Failure')]
    )

    def __str__(self):
        return f"Booking for {self.user.username} to {self.trip.destination.dest_name} on {self.trip.trip_date}"

   
    
class PassengerDetail(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='passenger_details')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=10)  # Optional phone number
    email = models.EmailField()  # Optional email

    def __str__(self):
        return f"Passenger {self.first_name} {self.last_name} for booking {self.booking.id}"


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE) 
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Feedback by {self.user.username} for {self.destination.country}'
    

class DummyCreditCard(models.Model):
    card_number = models.CharField(max_length=16, unique=True)  # 16-digit card number
    card_holder = models.CharField(max_length=100)  # Name on card
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=3)  # CVV code
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # Available balance

    def __str__(self):
        return f"{self.card_holder} - {self.card_number}"



class PaymentTransaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    card_holder = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)  # MM/YY format
    cvv = models.CharField(max_length=3)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[('success', 'Success'), ('failure', 'Failure')],
        default='failure'
    )
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for Booking {self.booking.id} - {self.payment_status}"






class Cancellation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    trip = models.ForeignKey('Booking', on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation by {self.user.username} for Trip {self.trip.id}"









