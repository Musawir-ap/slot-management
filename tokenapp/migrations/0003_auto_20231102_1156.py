# Generated by Django 4.2.6 on 2023-11-02 11:56

from django.db import migrations
from tokenapp.models import Status


def populate_status(apps, schema_editor):
    initial_statuses = ['Booked', 'Pending', 'Paid', 'Completed', 'Rejected', 'Payment Pending']
    for status in initial_statuses:
        Status.objects.get_or_create(name=status)

class Migration(migrations.Migration):

    dependencies = [
        ('tokenapp', '0002_status_remove_token_is_active_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_status),
    ]
