# Generated by Django 4.2 on 2024-05-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_alter_reservation_facilities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='facilities',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
