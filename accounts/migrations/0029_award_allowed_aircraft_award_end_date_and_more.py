# Generated by Django 5.0.2 on 2024-05-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_award_alter_evento_tipo_useraward'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='allowed_aircraft',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='award',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
