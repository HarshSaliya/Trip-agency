# Generated by Django 4.2.16 on 2024-11-02 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0019_rename_destination_detailed_desc_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailed_desc',
            name='country',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2024, 11, 2, 11, 9, 36, 11350, tzinfo=datetime.timezone.utc), max_length=19),
        ),
    ]
