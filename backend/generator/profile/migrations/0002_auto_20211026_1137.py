# Generated by Django 3.2.8 on 2021-10-26 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='experience',
        ),
        migrations.AddField(
            model_name='experience',
            name='since',
            field=models.DateField(default='1970-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experience',
            name='until',
            field=models.DateField(blank=True, null=True),
        ),
    ]