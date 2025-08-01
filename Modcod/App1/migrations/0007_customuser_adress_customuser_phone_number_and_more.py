# Generated by Django 5.1.7 on 2025-07-10 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0006_alter_project_etat_avancement'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='adress',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='ProfileImage',
            field=models.ImageField(default='profileimage/default.png', upload_to='profileimage/'),
        ),
    ]
