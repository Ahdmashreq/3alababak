# Generated by Django 2.2.6 on 2021-01-17 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210117_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseoder',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True),
        ),
    ]
