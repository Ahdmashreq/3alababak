# Generated by Django 2.2 on 2021-01-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_salesorder_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='discount_type',
            field=models.CharField(choices=[('percentage', '%'), ('amount', 'EGP')], default='percentage', max_length=11),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='shipping_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
