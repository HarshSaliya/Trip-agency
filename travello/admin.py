from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Destination, Detailed_desc, DayDescription

class DayDescriptionInline(admin.TabularInline):
    model = DayDescription
    extra = 1  # Allow one extra field for each entry

    def get_max_num(self, request, obj=None, **kwargs):
        """Limit the number of day descriptions based on the 'days' field in Detailed_desc."""
        if obj and obj.days:
            return obj.days
        return 0  # Return 0 if no days specified

class DetailedDescAdmin(admin.ModelAdmin):
    inlines = [DayDescriptionInline]

    def save_model(self, request, obj, form, change):
        """Ensure the number of day descriptions matches the 'days' value."""
        if obj.pk:  # If updating an existing object
            num_days = obj.days
            day_descriptions_count = obj.day_descriptions.count()

            if day_descriptions_count < num_days:
                # Allow saving with fewer day descriptions
                obj.save()
            else:
                # Raise error if more day descriptions than needed
                raise ValidationError(
                    f"You must enter exactly {num_days} day descriptions."
                )
        else:
            # For new objects, save directly
            super().save_model(request, obj, form, change)


# Register Destination without changes
admin.site.register(Destination)

# Register Detailed_desc with DetailedDescAdmin
admin.site.register(Detailed_desc, DetailedDescAdmin)
