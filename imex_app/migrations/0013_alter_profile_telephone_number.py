# Generated by Django 4.1 on 2023-05-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imex_app', '0012_remove_transporter_cover_image_transporter_vehicle_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
