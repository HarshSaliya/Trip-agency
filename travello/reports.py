from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from .models import *

def generate_destination_pdf(self, request, queryset):
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="destination_data_report.pdf"'

   
    pdf = SimpleDocTemplate(response, pagesize=letter)


    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("All Destination Data Report", styles['Title'])
    elements.append(title)

   
    data = [["ID", "Country", "Number of Places"]]

   
    for destination in queryset:
        data.append([destination.id, destination.country, destination.number])

   
    table = Table(data)

  
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTSIZE', (0, 0), (-1, -1), 12),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  
    ])
    table.setStyle(table_style)

  
    elements.append(table)

    pdf.build(elements)

    return response



def generate_user_pdf(self, request, queryset):
   pass


def generate_booking_pdf(self, request, queryset):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="booking_report.pdf"'

  
    pdf = SimpleDocTemplate(response, pagesize=letter)

    elements = []

    
    styles = getSampleStyleSheet()
    title = Paragraph("All Booking Data Report", styles['Title'])
    elements.append(title)

   
    data = [["User", "Destination", "Booking Date", "Trip Date", "Passengers", "Total Price", "Payment Status", "Passenger Name", "Passenger Age", "City"]]


    bookings = Booking.objects.all()
    for booking in bookings:
        data.append([
            booking.user.username,
            booking.destination.dest_name,
            booking.booking_date.strftime("%Y-%m-%d"),
            booking.trip_date.strftime("%Y-%m-%d"),
            booking.number_of_passengers,
            f"${booking.total_price:.2f}",
            booking.payment_status,
            f"{booking.passenger_first_name} {booking.passenger_last_name}",
            booking.passenger_age,
            booking.city
        ])

  
    table = Table(data)

  
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTSIZE', (0, 0), (-1, -1), 10),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  
        ('GRID', (0, 0), (-1, -1), 1, colors.black) 
    ])
    table.setStyle(table_style)

  
    elements.append(table)

  
    pdf.build(elements)

    return response