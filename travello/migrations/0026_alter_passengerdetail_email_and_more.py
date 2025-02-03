# Generated by Django 4.2.16 on 2024-11-13 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0025_passengerdetail_delete_pessanger_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passengerdetail',
            name='email',
            field=models.EmailField(default=12, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='passengerdetail',
            name='phone',
            field=models.CharField(default=12, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2024, 11, 13, 12, 30, 3, 628647, tzinfo=datetime.timezone.utc), max_length=19),
        ),
    ]
