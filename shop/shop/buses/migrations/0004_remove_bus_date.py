# Generated by Django 4.2.1 on 2023-05-22 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0003_bus_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='date',
        ),
    ]
