# Generated by Django 5.1.1 on 2024-10-04 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_estoquealmo_historicalestoquealmo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estoquealmo',
            options={'permissions': [('change_estoque_almo', 'Pode editar Estoque Almo')]},
        ),
        migrations.AlterModelOptions(
            name='estoqueat',
            options={'permissions': [('change_estoque_at', 'Pode editar Estoque AT')]},
        ),
    ]