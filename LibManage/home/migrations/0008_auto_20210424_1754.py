# Generated by Django 3.2 on 2021-04-24 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210424_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='system_variable_values',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_lost_penalty_amount', models.IntegerField(default=1000)),
                ('issue_period_expired_penalty', models.IntegerField(default=10)),
            ],
        ),
        migrations.AlterField(
            model_name='borrowedbook',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2021, 4, 24, 17, 54, 12, 423124)),
        ),
    ]
