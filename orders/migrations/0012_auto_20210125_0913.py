# Generated by Django 2.2.6 on 2021-01-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20210120_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseoder',
            name='purchase_code',
            field=models.CharField(blank=True, help_text='code number of a po', max_length=100, null=True, verbose_name='PO Number'),
        ),
        migrations.AlterField(
            model_name='purchaseoder',
            name='supplier_code',
            field=models.CharField(blank=True, help_text='code number of a supplier', max_length=250, null=True, verbose_name='Supplier PO Number'),
        ),
        migrations.AlterField(
            model_name='purchasetransaction',
            name='discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='tax',
            field=models.DecimalField(decimal_places=3, help_text='tax is saved as percentage', max_digits=4),
        ),
    ]