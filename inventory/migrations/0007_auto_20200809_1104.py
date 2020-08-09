# Generated by Django 2.2 on 2020-08-09 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0006_auto_20200806_1508'),
        ('inventory', '0006_auto_20200722_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='attribute',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productattribute',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stokeentry',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='stokeentry',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stoke_entry_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stokeentry',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='stokeentry',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stoketake',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='stoketake',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stoketake_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stoketake',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='stoketake',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brand',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brand',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemattributevalue',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_attribute_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemattributevalue',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='itemattributevalue',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_attribute_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uom',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uom_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uom',
            name='last_updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='uom',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
