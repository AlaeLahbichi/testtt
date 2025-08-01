# Generated by Django 5.1.7 on 2025-07-10 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ProfileImage',
            field=models.ImageField(default='profileimage/default.png', upload_to='profileimage/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Utilisateur', 'Utilisateur')], default='Utilisateur', max_length=20),
        ),
    ]
