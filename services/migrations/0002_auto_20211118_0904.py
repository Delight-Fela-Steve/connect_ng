# Generated by Django 3.2.9 on 2021-11-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
