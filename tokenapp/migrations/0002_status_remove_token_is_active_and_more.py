# Generated by Django 4.2.6 on 2023-11-02 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tokenapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='token',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='token',
            name='is_cancelled',
        ),
        migrations.RemoveField(
            model_name='token',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='token',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='token',
            name='is_rejected',
        ),
        migrations.CreateModel(
            name='StatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tokenapp.status')),
                ('tracked_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tokenapp.token')),
            ],
        ),
    ]
