from django.db import models
from django.conf import settings
from account.models import Company

# Create your models here.
class Location(models.Model):
    company = models.ForeignKey(Company,on_delete =models.CASCADE,)
    type = models.CharField(max_length  = 30)
    code =models.CharField(max_length  = 30)
    name =models.CharField(max_length  = 30)
    address =models.CharField(max_length  = 30,null=True,blank=True)
    city =models.CharField(max_length  = 30,null=True,blank=True)
    country = models.CharField(max_length  = 30,null=True,blank=True)
    zip_code =models.CharField(max_length  = 30,null=True,blank=True)
    phone_number =models.CharField(max_length  = 30,null=True,blank=True)
    landline =models.CharField(max_length  = 30,null=True,blank=True)
    number_of_products =models.IntegerField()
    manager_name=models.CharField(max_length  = 30)
    manager_mail =models.EmailField(null=True,blank=True)
    manager_phone_number=models.CharField(max_length  = 30)

    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True,auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="location_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
