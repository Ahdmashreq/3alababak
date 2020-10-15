from django.db import models
from django.conf import settings
from cities_light.models import Country, City


# Create your models here.
class Customer(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    landline = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='active', help_text='Checkbox if user is active')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="customer_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Supplier(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    landline = models.CharField(max_length=30, blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='active', help_text='Checkbox if user is active')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="supplier_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    landline = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="address_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        null=True, related_name= "address_last_updated_by")

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address


class Company(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.IntegerField(null=True, blank=True)
    last_updated_by = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
