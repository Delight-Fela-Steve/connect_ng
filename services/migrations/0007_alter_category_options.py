# Generated by Django 3.2.9 on 2021-11-18 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
