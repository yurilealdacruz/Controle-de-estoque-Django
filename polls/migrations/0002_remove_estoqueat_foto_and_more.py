# Generated by Django 4.0.6 on 2024-09-28 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estoqueat',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='historicalestoqueat',
            name='foto',
        ),
    ]
