# Generated by Django 4.2.16 on 2024-11-02 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0015_alter_detailed_desc_dest_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2024, 11, 2, 10, 51, 2, 52133, tzinfo=datetime.timezone.utc), max_length=19),
        ),
    ]
