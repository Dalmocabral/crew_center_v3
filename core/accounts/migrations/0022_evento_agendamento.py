# Generated by Django 5.0.2 on 2024-03-16 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_pirepsflight_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('tipo', models.CharField(choices=[('departures', 'Saida'), ('tipo2', 'Tipo 2'), ('tipo3', 'Tipo 3')], max_length=20)),
                ('aeroporto', models.CharField(blank=True, max_length=200, null=True)),
                ('data', models.DateField(blank=True, null=True)),
                ('hora', models.TimeField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('link_evento', models.URLField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(blank=True, max_length=200, null=True, verbose_name='Origem')),
                ('destino', models.CharField(blank=True, max_length=200, null=True, verbose_name='Destino')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('numero_voo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Número do Voo')),
                ('hora_partida', models.CharField(blank=True, default='N/D', max_length=200, null=True, verbose_name='Hora de Partida')),
                ('hora_chegada', models.CharField(blank=True, default='N/D', max_length=200, null=True, verbose_name='Hora de Chegada')),
                ('aeronave', models.CharField(blank=True, max_length=200, null=True, verbose_name='Aeronave')),
                ('gate', models.CharField(blank=True, default='N/D', max_length=200, null=True, verbose_name='Gate')),
                ('status', models.CharField(blank=True, choices=[('Partida Verde', 'Partida Verde'), ('Pousou Verde', 'Pousou Verde'), ('Partida Amarelo', 'Partida Amarelo'), ('Pousou Amarelo', 'Pousou Amarelo'), ('Partida Vermelho', 'Partida Vermelho'), ('Pousou Vermelho', 'Pousou Vermelho'), ('Agendado Cinza', 'Agendado Cinza'), ('Estimado Verde', 'Estimado Verde'), ('Cancelado Vermelho', 'Cancelado Vermelho')], default='Partida Verde', max_length=200, verbose_name='Status')),
                ('piloto', models.CharField(blank=True, max_length=200, null=True, verbose_name='Piloto')),
                ('usernames', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nomes de Usuário')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.evento', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
            },
        ),
    ]
