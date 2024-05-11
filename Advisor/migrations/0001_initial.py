# Generated by Django 4.2.2 on 2024-05-09 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Date and Time')),
                ('advisor', models.ForeignKey(limit_choices_to={'profile__account_type': 'advisor'}, on_delete=django.db.models.deletion.CASCADE, related_name='advisor_appointments', to=settings.AUTH_USER_MODEL, verbose_name='Advisor')),
                ('client', models.ForeignKey(limit_choices_to={'profile__account_type': 'normal'}, on_delete=django.db.models.deletion.CASCADE, related_name='client_appointments', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
        ),
    ]
