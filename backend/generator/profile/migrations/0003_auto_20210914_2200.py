# Generated by Django 3.2.7 on 2021-09-14 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='places_of_work',
        ),
        migrations.DeleteModel(
            name='PlaceOfWork',
        ),
    ]
