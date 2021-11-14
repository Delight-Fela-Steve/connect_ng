# Generated by Django 3.2.9 on 2021-11-14 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL),
        ),
    ]
