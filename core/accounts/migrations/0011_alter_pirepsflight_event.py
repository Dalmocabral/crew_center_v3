# Generated by Django 5.0.2 on 2024-03-04 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_pirepsflight_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirepsflight',
            name='event',
            field=models.CharField(choices=[('Não', 'Não'), ('Sim', 'Sim')], default='Não', max_length=50),
        ),
    ]
