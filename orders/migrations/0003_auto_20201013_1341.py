# Generated by Django 2.2 on 2020-10-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_inventory_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseoder',
            name='order_name',
            field=models.CharField(max_length=250),
        ),
    ]
