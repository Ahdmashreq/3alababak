# Generated by Django 2.2 on 2021-01-17 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesorder',
            name='order_name',
        ),
    ]
