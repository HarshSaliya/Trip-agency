# Generated by Django 4.2.16 on 2024-11-13 08:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0024_remove_booking_booking_date_booking_destination_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassengerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='pessanger_detail',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='city',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='passenger_age',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='passenger_first_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='passenger_last_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='trip_date',
        ),
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failure', 'Failure')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='booking',
            name='trip',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='travello.trip'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2024, 11, 13, 8, 28, 39, 620469, tzinfo=datetime.timezone.utc), max_length=19),
        ),
        migrations.AddField(
            model_name='passengerdetail',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_details', to='travello.booking'),
        ),
    ]
