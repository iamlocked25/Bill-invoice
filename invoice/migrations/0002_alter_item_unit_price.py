# Generated by Django 3.2.5 on 2022-03-02 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=16),
        ),
    ]
