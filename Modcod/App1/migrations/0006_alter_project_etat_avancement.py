# Generated by Django 5.1.7 on 2025-07-10 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0005_alter_project_delai_execution_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='etat_avancement',
            field=models.CharField(blank=True, choices=[('Refusée', 'Refusée'), ('Gagnée', 'Gagnée'), ('En cours de traitement', 'En cours de traitement'), ('Avant vente', 'Avant vente')], default='Avant vente', max_length=255, null=True),
        ),
    ]
