# Generated by Django 5.1.7 on 2025-07-11 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0007_customuser_adress_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='objet',
            new_name='object',
        ),
    ]
