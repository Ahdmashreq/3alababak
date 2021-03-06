# Generated by Django 2.2.6 on 2021-01-18 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=30, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('landline', models.CharField(blank=True, max_length=30, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('last_updated_by', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('landline', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.BooleanField(default=False, help_text='Checkbox if user is active', verbose_name='active')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True)),
                ('landline', models.CharField(blank=True, max_length=30, null=True)),
                ('status', models.BooleanField(default=False, help_text='Checkbox if user is active', verbose_name='active')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('last_updated_at', models.DateField(auto_now=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Company')),
            ],
        ),
    ]
