# Generated by Django 5.0.2 on 2024-06-18 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_award_link_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='allowed_aircraft',
        ),
        migrations.RemoveField(
            model_name='award',
            name='required_flights',
        ),
        migrations.CreateModel(
            name='AllowedAircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft', models.CharField(choices=[('A10', 'A10'), ('A318', 'A318'), ('A319', 'A319'), ('A320', 'A320'), ('A321', 'A321'), ('A333', 'A333'), ('A339', 'A339'), ('A33F', 'A33F'), ('A346', 'A346'), ('A359', 'A359'), ('A388', 'A388'), ('BCS3', 'BCS3'), ('B712', 'B712'), ('B737', 'B737'), ('B738', 'B738'), ('B739', 'B739'), ('B742', 'B742'), ('B744', 'B744'), ('B748', 'B748'), ('B74S', 'B74S'), ('B752', 'B752'), ('B763', 'B763'), ('B772', 'B772'), ('B77F', 'B77F'), ('B77L', 'B77L'), ('B77W', 'B77W'), ('B788', 'B788'), ('B789', 'B789'), ('B78X', 'B78X'), ('CC19', 'CC19'), ('C130', 'C130'), ('C30H', 'C30H'), ('C30J', 'C30J'), ('C17', 'C17'), ('C172', 'C172'), ('C208', 'C208'), ('CL35', 'CL35'), ('CRJ2', 'CRJ2'), ('CRJ7', 'CRJ7'), ('CRJ9', 'CRJ9'), ('CRJX', 'CRJX'), ('DC10', 'DC10'), ('DC1F', 'DC1F'), ('DHD8', 'DHD8'), ('E75S', 'E75S'), ('E75L', 'E75L'), ('E190', 'E190'), ('F14', 'F14'), ('F16', 'F16'), ('F18', 'F18'), ('F22', 'F22'), ('MD11', 'MD11'), ('MD1F', 'MD1F'), ('P38', 'P38'), ('SR22', 'SR22'), ('TBM9', 'TBM9')], max_length=5)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_aircrafts', to='accounts.award')),
            ],
        ),
        migrations.CreateModel(
            name='FlightLeg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_airport', models.CharField(max_length=4)),
                ('to_airport', models.CharField(max_length=4)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_legs', to='accounts.award')),
            ],
        ),
    ]
