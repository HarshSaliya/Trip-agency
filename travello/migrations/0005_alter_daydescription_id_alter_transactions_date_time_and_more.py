# Generated by Django 4.2.15 on 2024-09-16 07:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travello', '0004_remove_detailed_desc_day1_remove_detailed_desc_day2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daydescription',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2024, 9, 16, 7, 18, 51, 210958, tzinfo=datetime.timezone.utc), max_length=19),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('trip_date', models.DateField()),
                ('number_of_passengers', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('payment_status', models.CharField(default='Pending', max_length=20)),
                ('passenger_first_name', models.CharField(max_length=50)),
                ('passenger_last_name', models.CharField(max_length=50)),
                ('passenger_age', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travello.detailed_desc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
