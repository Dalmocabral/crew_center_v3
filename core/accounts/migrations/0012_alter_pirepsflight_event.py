# Generated by Django 5.0.2 on 2024-03-05 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_pirepsflight_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirepsflight',
            name='event',
            field=models.BooleanField(default=False),
        ),
    ]
