from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from cities_light.models import Country, City


class Customer(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, )
    slug = models.SlugField(null=True, blank=True, unique=True, allow_unicode=True)
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

    @property
    def full_name(self):
        """return first name concatenated with last name"""
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.id:
            # if the instance is being updated then it has an id
            obj = Customer.objects.get(id=self.id)
            # check if the user has changed the first name or last name
            if obj.first_name != self.first_name or obj.last_name != self.last_name:
                self.create_slug()
        else:
            # the instance is created for the first time
            self.create_slug()
        super(Customer, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugify(self.first_name + self.last_name + str(self.company.id))
        # cut_number = Customer.objects.filter(slug__startswith=self.slug).count()
        # slug_tail = cut_number + 1
        # self.slug = self.slug + str(slug_tail)


class Supplier(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, )
    slug = models.SlugField(null=True, blank=True, unique=True, allow_unicode=True)
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

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.id:
            obj = Supplier.objects.get(id=self.id)
            if obj.first_name != self.first_name or obj.last_name != self.last_name:
                self.create_slug()
        else:
            self.create_slug()
        super(Supplier, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugify(self.first_name + self.last_name + str(self.company.id))
        # supp_number = Supplier.objects.filter(slug__startswith=self.slug).count()
        # slug_tail = supp_number + 1
        # self.slug = self.slug + str(slug_tail)


class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True, related_name='address')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='supp_address')
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
                                        null=True, related_name="address_last_updated_by")

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

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
