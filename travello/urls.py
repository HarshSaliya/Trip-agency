from django.contrib import admin
from django.urls import path, include
from .reports import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),
    path('contact', views.contact, name='contact'),
    
    # Destination-related paths
    path('destination_list/<str:city_name>/', views.destination_list, name='destination_list'),
    path('destination_list/<str:city_name>/destination_details/<str:dest_name>/', views.destination_details, name='destination_details'),
    path('destination_list/<str:city_name>/destination_details/pessanger_detail_def/<str:dest_name>/', views.pessanger_detail_def, name='pessanger_detail_def'),
    path('upcoming_trips/', views.upcoming_trips, name='upcoming_trips'),

    path('get-available-dates/<str:city_name>/<str:dest_name>/', views.get_available_dates, name='get_available_dates'),

    path('passenger-detail/<str:city_name>/<str:dest_name>/', views.pessanger_detail_def, name='pessanger_detail_def'),
    # Payment and verification
    path('destination_list/destination_details/pessanger_detail_def/card_payment/', views.card_payment, name='card_payment'),
    path('destination_list/destination_details/pessanger_detail_def/otp_verification/', views.otp_verification, name='otp_verification'),
    path('destination_list/destination_details/pessanger_detail_def/net_payment/', views.net_payment, name='net_payment'),

    # About page
    path('about/', views.about, name='about'),
    path('my_trips/', views.my_trips, name='my_trips'),
    path('download_trip_pdf/<int:booking_id>/', views.download_trip_pdf, name='download_trip_pdf'),


    #whishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
   
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_wishlist/<str:city_name>/<str:dest_name>/', views.add_to_wishlist, name='add_to_wishlist'),


    #views
    path('search/', views.search_destinations, name='search_destinations'),
    #payment 
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment_processing/', views.payment_processing, name='payment_processing'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('subscribe/', views.subscribe, name='subscribe'),


 


    # Admin-related paths
    path('admin/generate_user_pdf/', generate_user_pdf, name='generate_user_pdf'),
    path('admin/generate_destination_pdf/', generate_destination_pdf, name='generate_destination_pdf'),
]




















# from django.contrib import admin
# from django.urls import path, include
# from .reports import *

# from . import views
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('register', views.register, name='register'),
#     path('login', views.login, name='login'),
#     path('logout', views.logout, name='logout'),
#     path('search', views.search, name='search'),
#     path('contact' , views.contact , name='contact'),
#     path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
#     path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
#     path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
#     path('destination_list/destination_details/pessanger_detail_def/<str:city_name>',views.pessanger_detail_def,name='pessanger_detail_def'),
#     path('upcoming_trips', views.upcoming_trips, name='upcoming_trips'),
#     path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/card_payment', views.card_payment, name='card_payment'),
#     path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/otp_verification', views.otp_verification, name='otp_verification'),
#     path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/net_payment', views.net_payment, name='net_payment'),
#     path('about/', views.about, name='about'),

#     path('contact/', views.contact, name='contact'),  

#     path('admin/generate_user_pdf/', generate_user_pdf, name='generate_user_pdf'),
#     path('admin/generate_destination_pdf/', generate_destination_pdf, name='generate_destination_pdf'),
# ]
