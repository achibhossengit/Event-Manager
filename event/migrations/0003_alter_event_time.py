# Generated by Django 5.1.6 on 2025-02-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_event_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
