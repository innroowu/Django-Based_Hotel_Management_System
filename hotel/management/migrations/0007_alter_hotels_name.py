# Generated by Django 4.2.11 on 2024-05-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20200808_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotels',
            name='name',
            field=models.CharField(default='test', max_length=30),
        ),
    ]
