# Generated by Django 2.2 on 2020-07-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='brand',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='itemattributevalue',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='itemattributevalue',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='itemattributevalue',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='itemattributevalue',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='uom',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='uom',
            name='created_by',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='uom',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='uom',
            name='updated_by',
            field=models.IntegerField(default=None),
        ),
    ]