# Generated by Django 3.0 on 2022-11-08 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imex_app', '0006_auto_20221104_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_air_port',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_sea_port',
            field=models.BooleanField(default=False),
        ),
    ]
