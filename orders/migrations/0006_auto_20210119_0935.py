# Generated by Django 2.2.6 on 2021-01-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210119_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialtransactionlines',
            name='transaction_type',
            field=models.CharField(choices=[('inbound', 'inbound'), ('outbound', 'outbound')], max_length=4),
        ),
    ]