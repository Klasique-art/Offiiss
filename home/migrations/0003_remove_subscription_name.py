# Generated by Django 4.1.3 on 2022-11-19 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='name',
        ),
    ]