from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from .reports import *

class DayDescriptionInline(admin.TabularInline):
    model = DayDescription
    extra = 1  

    def get_max_num(self, request, obj=None, **kwargs):
        """Limit the number of day descriptions based on the 'days' field in Detailed_desc."""
        if obj and obj.days:
            return obj.days
        return 0  

class DetailedDescAdmin(admin.ModelAdmin):
    inlines = [DayDescriptionInline]

    def save_model(self, request, obj, form, change):
        """Ensure the number of day descriptions matches the 'days' value."""
        if obj.pk:  
            num_days = obj.days
            day_descriptions_count = obj.day_descriptions.count()

            if day_descriptions_count < num_days:
                
                obj.save()
            else:
             
                raise ValidationError(
                    f"You must enter exactly {num_days} day descriptions."
                )
        else:

            super().save_model(request, obj, form, change)





class DestinationAdmin(admin.ModelAdmin):
    actions = ['download_pdf_report']

    def download_pdf_report(self, request, queryset):
        return generate_destination_pdf(self, request, queryset)

    download_pdf_report.short_description = 'Download PDF report for selected Destinations'

generate_booking_pdf.short_description = 'Download PDF report for selected Bookings'

class BookingAdmin(admin.ModelAdmin):
    actions = [generate_booking_pdf]
    

admin.site.register(Booking, BookingAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Detailed_desc, DetailedDescAdmin)
admin.site.register(ContactUs)
admin.site.register(Wishlist)
admin.site.register(Trip)
admin.site.register(City)
admin.site.register(DummyCreditCard)
admin.site.register(PassengerDetail)
admin.site.register(PaymentTransaction)
admin.site.register(Subscriber)
