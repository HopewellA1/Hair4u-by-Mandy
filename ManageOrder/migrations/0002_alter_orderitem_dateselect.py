# Generated by Django 4.1.7 on 2023-07-23 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManageOrder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='DateSelect',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 14, 24, 51, 176317)),
        ),
    ]
