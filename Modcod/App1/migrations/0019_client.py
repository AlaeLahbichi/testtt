# Generated by Django 5.1.7 on 2025-07-21 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0018_logs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
            ],
        ),
    ]
