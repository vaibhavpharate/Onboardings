# Generated by Django 4.2.9 on 2024-01-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0003_clients_plans'),
    ]

    operations = [
        migrations.AddField(
            model_name='site_configs',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]