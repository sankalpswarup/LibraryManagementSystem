# Generated by Django 3.2 on 2021-04-21 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210422_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 22, 3, 30, 34, 403063)),
        ),
    ]
