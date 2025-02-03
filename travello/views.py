from django.shortcuts import render
from .models import *

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import render, redirect , get_object_or_404
from .models import Booking, Detailed_desc
from django.forms import formset_factory
from django.core.paginator import Paginator  # show dest in row and columns
from django.http import JsonResponse

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import random
import string





import random



def index(request):
    dests = Destination.objects.all()
    dest1 = []
    for i in range(6):
        j = (i + 1) * 2 
        try:
            temp = Detailed_desc.objects.get(dest_id=j)
            dest1.append(temp)
        except Detailed_desc.DoesNotExist:
            print(f"No Detailed_desc found with dest_id={j}")
            continue

    return render(request, 'index.html', {'dests': dests, 'dest1': dest1})


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)
                user.save()
                messages.info(request, 'User created successfully!')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

       
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.info(request, 'Email not found')
            return redirect('login')

        user = auth.authenticate(username=user.username, password=password)

        if user is not None:
            if user.is_active: 
                auth.login(request, user)
                # messages.info(request, 'Successfully Logged in')

               
                email = request.user.email
                print(email)
                content = f'Hello {request.user.first_name} {request.user.last_name},\nYou are logged in to our site. Keep connected and keep traveling.'
               
                dests = Destination.objects.all()
                return render(request, 'index.html', {'dests': dests})
            else:
                messages.info(request, 'Account is inactive')
                return redirect('login')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')



def home(request):
     return redirect('index')


def upcoming_trips(request):
    # Fetch all destinations
    dests = Destination.objects.all()
    
    # Fetch details for each destination
    detailed_descs = Detailed_desc.objects.all()
    
    context = {
        'dests': dests,
        'detailed_descs': detailed_descs
    }
    return render(request, 'upcoming_trip.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create a new ContactUs instance
        contact = ContactUs(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')  # Redirect to the same page or another page after successful submission

    return render(request, 'contact.html')  # Replace with your actual template name


def logout(request):
    auth.logout(request)
    return redirect('index')


def forgot_password(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.first_name != first_name:
                messages.error(request, "First name doesn't match the email address.")
                return redirect('forgot_password')
            
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(new_password)
            # user.profile.password_reset_expiration = now() + timedelta(minutes=30)
            # user.profile.save()
            user.save()

            # Send the new password to the user's email
            subject = "Your New Password"
            subject = "Your Temporary Password"
            message = (
                f"Hello {user.first_name} {user.last_name},\n\n"
                f"Your new temporary password is: {new_password}\n\n"
                f"⚠️ Please note:\n"
                f"1. Do not share this password with anyone.\n"
                f"2. This password will expire in 30 minutes if not used.\n\n"
                f"After logging in, ensure you change your password for security reasons.\n\n"
                f"Best regards,\nYour Support Team"
            )
            from_email = 'your_email@gmail.com'  
            send_mail(subject, message, from_email, [email])

            messages.success(request, "A new password has been sent to your email address.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
            return redirect('forgot_password')
    return render(request, 'login.html')


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email is not already in the database
        if not Subscriber.objects.filter(email=email).exists():
            Subscriber.objects.create(email=email)
    
    return redirect('/')


@login_required
def my_trips(request):
    # Fetch bookings for the logged-in user
    user_bookings = Booking.objects.filter(user=request.user).select_related('trip', 'trip__destination', 'trip__city')
    context = {
        'bookings': user_bookings,
    }
    return render(request, 'my_trips.html', context)

@login_required
def download_trip_pdf(request, booking_id):
    # Fetch the booking object
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Fetch related models' data (like passenger details, payment info, trip details)
    passenger_details = PassengerDetail.objects.filter(booking=booking)
    payment_info = PaymentTransaction.objects.filter(booking=booking).first()  # Assuming there's one payment per booking
    trip_details = booking.trip
    destination_details = trip_details.destination
    city_details = trip_details.city
    
    # Fetch credit card details (you can customize this if needed)
    credit_card_info = DummyCreditCard.objects.filter(card_holder=payment_info.card_holder).first()
    
    # Sample terms and conditions, you can customize this based on your requirements
    terms_and_conditions = """
        1. Arrive at the destination at least 2 hours before the trip starts.
        2. All payments are non-refundable.
        3. Ensure that all personal documents are in order before traveling.
        4. Make sure you have travel insurance for the duration of the trip.
        5. Failure to adhere to the booking terms may result in cancellations without refunds.
    """
    
    # Prepare the context with all the details
    context = {
        'booking': booking,
        'passenger_details': passenger_details,
        'payment_info': payment_info,
        'trip_details': trip_details,
        'destination_details': destination_details,
        'city_details': city_details,
        'credit_card_info': credit_card_info,
        'terms_and_conditions': terms_and_conditions,
    }
    
    # Render the template to HTML
    html = render_to_string('pdf_template.html', context)
    
    # Create a response with content type as PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trip_{booking_id}.pdf"'

    # Use xhtml2pdf's pisa to convert HTML to PDF and write to the response
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Check for errors in PDF generation
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    return response







@login_required(login_url='login')
def destination_list(request, city_name):
    dests = Detailed_desc.objects.filter(country=city_name)
    return render(request, 'travel_destination.html', {'dests': dests})

def destination_details(request, city_name, dest_name):
    # Retrieve the destination based on both `city_name` and `dest_name`
    dest = get_object_or_404(Detailed_desc, country=city_name, dest_name=dest_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request, 'destination_details.html', {'dest': dest})

def search(request):
    try:
        place1 = request.session.get('place')
        dest = Detailed_desc.objects.get(dest_name=place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except Detailed_desc.DoesNotExist:
        messages.info(request, 'Place not found')
        return redirect('index')

class KeyValueForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.IntegerField()

def pessanger_detail_def1(request, city_name, dest_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    
    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        if formset.is_valid():
            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')
            
            # Fetch the destination based on dest_name
            destination = get_object_or_404(Detailed_desc, dest_name=dest_name)
            user = request.user
            city = request.session.get('city', 'Unknown')  

            for form in formset:
                if form.cleaned_data:
                    Booking.objects.create(
                        user=user,
                        destination=destination,
                        trip_date=temp_date,
                        number_of_passengers=formset.total_form_count(),
                        total_price=request.session.get('price', 0),
                        passenger_first_name=form.cleaned_data['first_name'],
                        passenger_last_name=form.cleaned_data['last_name'],
                        passenger_age=form.cleaned_data['age'],
                        city=city
                    )
            
            no_of_person = formset.total_form_count()
            price1 = no_of_person * request.session.get('price', 0)
            GST = price1 * 0.18
            final_total = round(price1 + GST, 2)  # Round for two decimal places
            request.session['pay_amount'] = final_total
            
            return render(request, 'payment.html', {
                'no_of_person': no_of_person,
                'price1': price1,
                'GST': round(GST, 2),
                'final_total': final_total,
                'city': city
            })
    else:
        formset = KeyValueFormSet()
        return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, 'dest_name': dest_name})

#on workoing





# New function to fetch available dates
# Fetch available dates for a city
# def get_available_dates(request, city_name):
#     trips = Trip.objects.filter(city__name=city_name)
#     dates = [trip.trip_date.strftime('%Y-%m-%d') for trip in trips]
#     return JsonResponse({'dates': dates})




def get_available_dates(request, city_name, dest_name):
    try:
        # Get the city and destination objects based on the names
        city = City.objects.get(name=city_name)
        destination = Detailed_desc.objects.get(dest_name=dest_name)

        # Filter trips by both city and destination
        trips = Trip.objects.filter(city=city, destination=destination)
        available_dates = trips.values_list('trip_date', flat=True)
        
        # Convert dates to a list and return as JSON
        dates_list = list(available_dates)
        return JsonResponse({'dates': dates_list})
    except (City.DoesNotExist, Detailed_desc.DoesNotExist):
        return JsonResponse({'dates': []})
    
    

# def pessanger_detail_def(request, city_name, dest_name):
#     KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
#     cities = City.objects.all()  # Fetch all cities to display in the dropdown
    
#     if request.method == 'POST':
#         formset = KeyValueFormSet(request.POST)
#         if formset.is_valid():
#             temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
#             date1 = datetime.now().date()
#             if temp_date < date1:
#                 return redirect('index')
            
#             destination = get_object_or_404(Detailed_desc, dest_name=dest_name)
#             city = get_object_or_404(City, name=request.POST['city'])
#             user = request.user

#             for form in formset:
#                 if form.cleaned_data:
#                     Booking.objects.create(
#                         user=user,
#                         destination=destination,
#                         trip_date=temp_date,
#                         city=city,
#                         number_of_passengers=formset.total_form_count(),
#                         total_price=request.session.get('price', 0),
#                         passenger_first_name=form.cleaned_data['first_name'],
#                         passenger_last_name=form.cleaned_data['last_name'],
#                         passenger_age=form.cleaned_data['age']
#                     )

#             no_of_person = formset.total_form_count()
#             price1 = no_of_person * request.session.get('price', 0)
#             GST = price1 * 0.18
#             final_total = round(price1 + GST, 2)
#             request.session['pay_amount'] = final_total

#             return render(request, 'sample.html', {
#                 'no_of_person': no_of_person,
#                 'price1': price1,
#                 'GST': round(GST, 2),
#                 'final_total': final_total,
#                 'cities': cities,
#                 'formset': KeyValueFormSet()
#             })
#     else:
#         formset = KeyValueFormSet()
    
#     return render(request, 'sample.html', {'formset': formset, 'city_name': city_name, 'dest_name': dest_name, 'cities': cities})


from django import forms

# Form for collecting passenger details
class KeyValueForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )
    age = forms.IntegerField(
        required=True,
        min_value=10,  # Minimum age validation
        max_value=120,  # Maximum age validation
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'})
    )
    phone = forms.CharField(
        max_length=10,
        required=True,  # Make it required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Phone Number',
            'pattern': '[0-9]{10}',  # Regex for a valid 10-digit phone number
            'title': 'Enter a valid 10-digit phone number'
        })
    )
    email = forms.EmailField(
        required=True,  # Make it required
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )

from django.shortcuts import redirect

def pessanger_detail_def(request, city_name, dest_name):
    KeyValueFormSet = formset_factory(KeyValueForm, extra=1)
    cities = City.objects.all()  # Fetch all cities to display in the dropdown
    destinations = Detailed_desc.objects.all()  # Fetch all destinations

    if request.method == 'POST':
        formset = KeyValueFormSet(request.POST)
        
        if formset.is_valid():
            # Debug: Print the formset cleaned data to ensure data is valid
            print(f'Formset cleaned data: {formset.cleaned_data}')

            temp_date = datetime.strptime(request.POST['trip_date'], "%Y-%m-%d").date()
            date1 = datetime.now().date()
            if temp_date < date1:
                return redirect('index')

            # Get the destination and city objects based on form data
            destination = get_object_or_404(Detailed_desc, dest_name=dest_name)
            city = get_object_or_404(City, name=request.POST['city'])
            trip_date = request.POST['trip_date']  # Get trip date from the form

            # Get the trip based on city, destination, and date
            trip = Trip.objects.get(city=city, destination=destination, trip_date=trip_date)

            # Get the total number of passengers from the form
            number_of_passengers = int(request.POST['num_passengers'])

            # Calculate the price with GST (18%)
            price_per_person = destination.price
            gst_percentage = 18  # 18% GST
            total_price_before_gst = price_per_person * number_of_passengers
            gst_amount = (gst_percentage / 100) * total_price_before_gst
            total_price = total_price_before_gst + gst_amount

            # Create the booking instance
            booking = Booking.objects.create(
                user=request.user,
                trip=trip,
                number_of_passengers=number_of_passengers,
                total_price=total_price,
                payment_status='pending'
            )

            # Store passenger details
            for form in formset:
                if form.cleaned_data:
                    PassengerDetail.objects.create(
                        booking=booking,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        age=form.cleaned_data['age'],
                        phone=form.cleaned_data.get('phone'),
                        email=form.cleaned_data.get('email')
                    )

            # Debug: Print booking details to verify
            print(f'Booking created with ID: {booking.id}, Total Price: {total_price}')

            # Store the total price (with GST) and booking ID in session for payment
            request.session['pay_amount'] = total_price
            request.session['order_id'] = booking.id

            # Redirect to payment page
            return redirect('payment_page', booking_id=booking.id)

        else:
            print(f'Formset errors: {formset.errors}')
            return render(request, 'sample.html', {
                'formset': formset,
                'city_name': city_name,
                'dest_name': dest_name,
                'cities': cities,
                'destinations': destinations
            })

    else:
        formset = KeyValueFormSet()

    return render(request, 'sample.html', {
        'formset': formset,
        'city_name': city_name,
        'dest_name': dest_name,
        'cities': cities,
        'destinations': destinations
    })





@login_required
def add_to_wishlist(request, city_name, dest_name):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your wishlist.")
        return redirect('login')  # Redirect to the login page if not authenticated
    
    try:
        # Attempt to fetch the Detailed_desc instance
        detailed_desc = Detailed_desc.objects.get(dest_name=dest_name, country=city_name)

        # Check if the user already has this destination in their wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            destination=detailed_desc
        )

        if created:
            messages.success(request, f'{detailed_desc.dest_name} has been added to your wishlist!')
        else:
            messages.info(request, f'{detailed_desc.dest_name} is already in your wishlist.')

    except Detailed_desc.DoesNotExist:
        messages.error(request, 'The specified destination does not exist.')
        return redirect('destination_list')  # Redirect to an appropriate error page or list of destinations

    return redirect('destination_details', city_name=city_name, dest_name=dest_name)

from django.db.models import Q
from django.shortcuts import render
from .models import Destination, Detailed_desc

def search_destinations(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search for both country and destination name
        dests = Detailed_desc.objects.filter(
            Q(country__icontains=query) | Q(dest_name__icontains=query)  # Case-insensitive search for country or dest_name
        )
    else:
        dests = Detailed_desc.objects.all()  # Return all destinations if no search query is provided
    
    return render(request, 'upcoming_trip.html', {'dests': dests})



@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, item_id):
    try:
        wishlist_item = Wishlist.objects.get(id=item_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, "Item removed from wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('wishlist')





def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        card_holder = request.POST['card_holder']
        card_number = request.POST['card_number']
        expiry_date = request.POST['expiry_date']
        cvv = request.POST['cvv']
        amount_to_pay = booking.total_price

        # Validate card details (Check in DummyCreditCard table)
        try:
            credit_card = DummyCreditCard.objects.get(card_number=card_number, cvv=cvv, expiry_date=expiry_date)
            
            # Check if the card has sufficient balance
            if credit_card.balance >= amount_to_pay:
                # Deduct the amount
                credit_card.balance -= amount_to_pay
                credit_card.save()

                # Save payment transaction as success
                PaymentTransaction.objects.create(
                    booking=booking,
                    card_holder=card_holder,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    amount_paid=amount_to_pay,
                    payment_status='success'
                )

                # Update booking payment status
                booking.payment_status = 'successful'
                booking.save()

                messages.success(request, 'Payment successful! Your booking is confirmed.')
            else:
                # Insufficient balance
                PaymentTransaction.objects.create(
                    booking=booking,
                    card_holder=card_holder,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    amount_paid=amount_to_pay,
                    payment_status='failure'
                )

                messages.error(request, 'Payment failed due to insufficient balance.')

        except DummyCreditCard.DoesNotExist:
            # Invalid card details
            messages.error(request, 'Invalid card details. Please try again.')

        return redirect('payment_page', booking_id=booking_id)

    return render(request, 'payment.html', {'booking': booking})





def payment_processing(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)

        # Process the payment here...
        booking.payment_status = 'successful'  # Example update
        booking.save()

        return HttpResponseRedirect(reverse('payment_page', args=[booking_id]))
    else:
        return HttpResponseRedirect('/')



def mock_payment(request):
    # Capture the booking_id and pay_amount from the GET parameters
    booking_id = request.GET.get('booking_id')
    pay_amount = Decimal(request.GET.get('pay_amount'))  # Convert pay_amount to Decimal

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_holder = request.POST.get('card_holder')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Verify card details
        try:
            card = DummyCreditCard.objects.get(
                card_number=card_number,
                card_holder=card_holder,
                expiry_date=expiry_date,
                cvv=cvv
            )

            # Check if balance is sufficient
            if card.balance >= pay_amount:
                # Deduct amount
                card.balance -= pay_amount  # Now both are Decimal
                card.save()

                # Record payment as successful
                MockPayment.objects.create(order_id=booking_id, amount=pay_amount, status='Success')
                payment_status = 'success'
                message = 'Payment successful!'
            else:
                # Insufficient balance
                MockPayment.objects.create(order_id=booking_id, amount=pay_amount, status='Failed')
                payment_status = 'failure'
                message = 'Payment failed! Insufficient balance.'
        except DummyCreditCard.DoesNotExist:
            payment_status = 'failure'
            message = 'Invalid credit card details!'

        return render(request, 'payment.html', {'payment_status': payment_status, 'message': message, 'order_id': booking_id, 'pay_amount': pay_amount})

    # Render the payment page with the booking_id and total_price (pay_amount)
    return render(request, 'payment.html', {'order_id': booking_id, 'pay_amount': pay_amount})




























































@login_required(login_url='login')
def card_payment(request):
    card_no = request.POST.get('card_number')
    pay_method = 'Debit card'
    MM = request.POST['MM']
    YY = request.POST['YY']
    CVV = request.POST['cvv']

    request.session['dcard'] = card_no
    try:
        balance = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).Balance
        request.session['total_balance'] = balance
        mail1 = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).email

        if int(balance) >= int(request.session['pay_amount']):
            # print("if ma gayu")
            rno = random.randint(100000, 999999)
            request.session['OTP'] = rno

            amt = request.session['pay_amount']
            username = request.user.get_username()
            print(username)
            user = User.objects.get(username=username)
            mail_id = user.email
            print([mail_id])
            msg = 'Your OTP For Payment of ₹' + str(amt) + ' is ' + str(rno)
            # print(msg)
            # print([mail_id])
            # print(amt)
            send_mail('OTP for Debit card Payment',
                      msg,
                      'travellotours89@gmail.com',
                      [mail_id],
                      fail_silently=False)
            return render(request, 'OTP.html')
        return render(request, 'wrongdata.html')


    except:
        return render(request, 'wrongdata.html')
    
















































































@login_required(login_url='login')
def net_payment(request):
    username = request.POST['cardNumber']
    Password1 = request.POST['pass']
    Bank_name = request.POST['banks']
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Net Banking'
    try:
        r = NetBanking.objects.get(Username=username, Password=Password1,Bank=Bank_name)
        balance = r.Balance
        request.session['total_balance'] = balance
        if int(balance) >= int(request.session['pay_amount']):
            total_balance = int(request.session['total_balance'])
            rem_balance = int(total_balance - int(request.session["pay_amount"]))
            r.Balance = rem_balance
            r.save(update_fields=['Balance'])
            r.save()
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
            t.save()
            return render(request, 'confirmetion_page.html')
        else:
            t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
            t.save()
            return render(request, 'wrongdata.html')
    except :
        return render(request, 'wrongdata.html')

@login_required(login_url='login')
def otp_verification(request):
    otp1 = int(request.POST['otp'])
    usernameget = request.user.get_username()
    Trip_same_id1 = request.session['Trip_same_id']
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance-int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method, Status='Successfull')
        t.save()
        z = pessanger_detail.objects.all().filter(Trip_same_id=Trip_same_id1)
        for obj in z:
            obj.pay_done = 1
            obj.save(update_fields=['pay_done'])
            obj.save()
            print(obj.pay_done)
        return render(request, 'confirmetion_page.html')
    else:
        t = Transactions(username=usernameget, Trip_same_id=Trip_same_id1, Amount=amt, Payment_method=pay_method)
        t.save()
        return render(request, 'wrong_OTP.html')

@login_required(login_url='login')
def data_fetch(request):
    username = request.user.get_username()
    person = pessanger_detail.objects.all().filter(username=username)



#afret

def about(request):
    return render(request, 'about.html')
