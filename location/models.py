from django.db import models
from django.conf import settings
from account.models import Company
from cities_light.models import Country, City
from django.template.defaultfilters import slugify

# Create your models here.
from alababak.utils import arabic_slugify
from alababak.utils import get_seq


class Location(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    slug = models.SlugField(null=True, blank=True, unique=True, allow_unicode=True)
    type = models.CharField(max_length=30, choices=[('w', 'warehouse'), ('s', 'store')], blank=False)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    landline = models.CharField(max_length=30, null=True, blank=True)
    number_of_products = models.IntegerField(null=True, blank=True)
    manager_name = models.CharField(max_length=30, null=True, blank=True)
    manager_mail = models.EmailField(null=True, blank=True)
    manager_phone_number = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="location_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            if self.type == 'w':
                rows_number = Location.objects.filter(type='w', company=self.company).count()
                self.code = "W-" + get_seq(rows_number) + '-' + str(self.company.id)
            elif self.type == 's':
                rows_number = Location.objects.filter(type='s', company=self.company).count()
                self.code = "S-" + get_seq(rows_number) + '-' + str(self.company.id)
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.code)

        super(Location, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugify(self.code)
        location_number = Location.objects.filter(slug__startswith=self.slug).count()
        if location_number != 0:
            slug_tail = location_number + 1
            self.slug = self.slug + '-' + str(slug_tail)
