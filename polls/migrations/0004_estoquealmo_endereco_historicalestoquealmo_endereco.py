# Generated by Django 5.1.1 on 2024-10-04 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_estoquealmo_options_alter_estoqueat_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='estoquealmo',
            name='endereco',
            field=models.CharField(default='Lugar nenhum', max_length=255),
        ),
        migrations.AddField(
            model_name='historicalestoquealmo',
            name='endereco',
            field=models.CharField(default='Lugar nenhum', max_length=255),
        ),
    ]
