# Generated by Django 2.2.6 on 2021-01-14 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseoder',
            name='order_name',
        ),
    ]
