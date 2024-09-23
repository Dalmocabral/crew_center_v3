# Generated by Django 5.0.2 on 2024-03-03 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirepsflight',
            name='aircraft',
            field=models.CharField(choices=[('A-10', 'A-10'), ('AC-130', 'AC-130'), ('Airbus A220-300', 'Airbus A220-300'), ('Airbus A318', 'Airbus A318'), ('Airbus A319', 'Airbus A319'), ('Airbus A320', 'Airbus A320'), ('Airbus A321', 'Airbus A321'), ('Airbus A330-200F', 'Airbus A330-200F'), ('Airbus A330-300', 'Airbus A330-300'), ('Airbus A330-900', 'Airbus A330-900'), ('Airbus A340-600', 'Airbus A340-600'), ('Airbus A350', 'Airbus A350'), ('Airbus A380', 'Airbus A380'), ('Boeing 717-200', 'Boeing 717-200'), ('Boeing 737-700', 'Boeing 737-700'), ('Boeing 737-800', 'Boeing 737-800'), ('Boeing 737-900', 'Boeing 737-900'), ('Boeing 747-200', 'Boeing 747-200'), ('Boeing 747-400', 'Boeing 747-400'), ('Boeing 747-8', 'Boeing 747-8'), ('Boeing 747-AF1', 'Boeing 747-AF1'), ('Boeing 747-SCA', 'Boeing 747-SCA'), ('Boeing 747-SOFIA', 'Boeing 747-SOFIA'), ('Boeing 757-200', 'Boeing 757-200'), ('Boeing 767-300', 'Boeing 767-300'), ('Boeing 777-200ER', 'Boeing 777-200ER'), ('Boeing 777-200LR', 'Boeing 777-200LR'), ('Boeing 777-300ER', 'Boeing 777-300ER'), ('Boeing 777F', 'Boeing 777F'), ('Boeing 787-10', 'Boeing 787-10'), ('Boeing 787-8', 'Boeing 787-8'), ('Boeing 787-9', 'Boeing 787-9'), ('Bombardier Dash 8-Q400', 'Bombardier Dash 8-Q400'), ('C-130H', 'C-130H'), ('C-130J', 'C-130J'), ('C-130J-30', 'C-130J-30'), ('C-17', 'C-17'), ('CRJ-1000', 'CRJ-1000'), ('CRJ-200', 'CRJ-200'), ('CRJ-700', 'CRJ-700'), ('CRJ-900', 'CRJ-900'), ('Cessna 172', 'Cessna 172'), ('Cessna 208', 'Cessna 208'), ('Challenger 350', 'Challenger 350'), ('Cirrus SR22 GTS', 'Cirrus SR22 GTS'), ('CubCrafters XCub', 'CubCrafters XCub'), ('DC-10', 'DC-10'), ('DC-10F', 'DC-10F'), ('E175', 'E175'), ('E190', 'E190'), ('F-14', 'F-14'), ('F-16', 'F-16'), ('F-22', 'F-22'), ('F/A-18E Super Hornet', 'F/A-18E Super Hornet'), ('MD-11', 'MD-11'), ('MD-11F', 'MD-11F'), ('P-38', 'P-38'), ('Space Shuttle', 'Space Shuttle'), ('Spitfire', 'Spitfire'), ('TBM-930', 'TBM-930')], max_length=50),
        ),
    ]
