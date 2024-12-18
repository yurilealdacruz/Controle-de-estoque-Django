# Generated by Django 5.1.1 on 2024-10-05 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_estoque_adicao_historicalestoque_adicao_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstoqueHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_adicionada', models.IntegerField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('estoque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.estoque')),
            ],
        ),
    ]
