# Generated by Django 2.2 on 2020-10-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20201013_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_balance',
            name='qnt',
            field=models.IntegerField(default=0),
        ),
    ]
