# Generated by Django 3.2 on 2021-04-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_books_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=100)),
                ('pword', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=250)),
            ],
        ),
    ]
