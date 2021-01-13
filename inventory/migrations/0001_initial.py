# Generated by Django 2.2.6 on 2021-01-13 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20210113_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('att_type', models.CharField(choices=[('text', 'text'), ('number', 'number'), ('date', 'date'), ('checkbox', 'checkbox')], max_length=50, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('display_name', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=30, null=True)),
                ('barcode', models.CharField(blank=True, max_length=30, null=True)),
                ('expirable', models.BooleanField(default=False, help_text='Checkbox if item is expirable', verbose_name='Expirable')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StokeEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UomCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Company')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uom_category_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Uom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('reference', 'Reference Unit of Measure of this category'), ('smaller', 'Smaller Than The Reference Unit of Measure '), ('bigger', 'Bigger Than The Reference Unit of Measure')], max_length=30)),
                ('ratio', models.DecimalField(blank=True, decimal_places=2, help_text='A content for this thing', max_digits=14, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uoms', to='inventory.UomCategory')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Company')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uom_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StokeTake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('location', 'By Location'), ('category', 'By Category'), ('random', 'Random')], default='location', max_length=30)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Drafted', 'Drafted'), ('In Progress', 'In Progress'), ('Pending Approval', 'Pending Approval'), ('Approved', 'Approved'), ('Done', 'Done')], default='Drafted', max_length=30)),
                ('random_number', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stoke_category', to='inventory.Category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Company')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stoketake_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
