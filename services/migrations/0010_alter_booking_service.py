# Generated by Django 3.2.9 on 2021-11-20 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_booking_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
    ]
