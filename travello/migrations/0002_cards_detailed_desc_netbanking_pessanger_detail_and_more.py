# Generated by Django 4.2.15 on 2024-09-13 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('Card_number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Ex_month', models.CharField(max_length=2)),
                ('Ex_Year', models.CharField(max_length=2)),
                ('CVV', models.CharField(max_length=3)),
                ('Balance', models.CharField(max_length=8)),
                ('email', models.EmailField(default='rambarodavala21@gmail.com', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Detailed_desc',
            fields=[
                ('dest_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=20)),
                ('days', models.IntegerField(default=5)),
                ('price', models.IntegerField(default=20000)),
                ('rating', models.IntegerField(default=5)),
                ('dest_name', models.CharField(max_length=25)),
                ('img1', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(upload_to='pics')),
                ('desc', models.TextField()),
                ('day1', models.CharField(max_length=200)),
                ('day2', models.CharField(max_length=200)),
                ('day3', models.CharField(max_length=200)),
                ('day4', models.CharField(max_length=200)),
                ('day5', models.CharField(max_length=200)),
                ('day6', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='NetBanking',
            fields=[
                ('Username', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Password', models.CharField(max_length=14)),
                ('Bank', models.CharField(max_length=25)),
                ('Balance', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='pessanger_detail',
            fields=[
                ('Trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('Trip_same_id', models.IntegerField(default=1)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('age', models.IntegerField(default=10)),
                ('username', models.CharField(max_length=10)),
                ('Trip_date', models.DateField()),
                ('payment', models.IntegerField(default=50)),
                ('city', models.CharField(max_length=20)),
                ('pay_done', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('Transactions_ID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10)),
                ('Trip_same_id', models.IntegerField(default=1)),
                ('Amount', models.CharField(max_length=8)),
                ('Status', models.CharField(default='Failed', max_length=15)),
                ('Payment_method', models.CharField(blank=True, max_length=15)),
                ('Date_Time', models.CharField(default=datetime.datetime(2024, 9, 13, 8, 27, 12, 132025, tzinfo=datetime.timezone.utc), max_length=19)),
            ],
        ),
        migrations.AddField(
            model_name='destination',
            name='number',
            field=models.IntegerField(default=2),
        ),
    ]
