# Generated by Django 2.2.6 on 2021-01-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20210119_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseoder',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True),
        ),
    ]
