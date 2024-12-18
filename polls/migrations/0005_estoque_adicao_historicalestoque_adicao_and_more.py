# Generated by Django 5.1.1 on 2024-10-05 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_estoquealmo_endereco_historicalestoquealmo_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='estoque',
            name='adicao',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalestoque',
            name='adicao',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='estoquealmo',
            name='endereco',
            field=models.CharField(default='Sem registro de localização', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalestoquealmo',
            name='endereco',
            field=models.CharField(default='Sem registro de localização', max_length=255),
        ),
    ]
