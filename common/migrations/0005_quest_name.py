# Generated by Django 5.0.6 on 2024-06-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_dialoglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='quest',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
