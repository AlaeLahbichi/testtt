# Generated by Django 5.1.7 on 2025-07-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_customuser_profileimage_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ProfileImage',
            field=models.ImageField(default='image/default.png', upload_to='profileimage/'),
        ),
    ]
