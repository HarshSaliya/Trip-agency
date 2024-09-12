# Generated by Django 3.0.4 on 2020-04-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0009_auto_20200428_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('Card_number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Ex_month', models.CharField(max_length=2)),
                ('Ex_Year', models.CharField(max_length=2)),
                ('CVV', models.CharField(max_length=3)),
                ('Balance', models.CharField(max_length=5)),
                ('email', models.EmailField(default='devaniurvish881@gmail.com', max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='pessanger_all_detail',
        ),
    ]
