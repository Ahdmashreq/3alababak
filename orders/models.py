from django.db import models
from djmoney.models.fields import MoneyField
from account.models import Supplier, Customer, Company
from inventory.models import Item
from django.conf import settings


# Create your models here.
class PurchaseOder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, )
    code = models.CharField(max_length=10)
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP', null=True, blank=True)
    status = models.CharField(max_length=8,
                              choices=[('received', 'Received'), ('returned', 'Returned'), ('shipping', 'Shipping')])
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="purchase_order_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.code


class SalesOrder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    code = models.CharField(max_length=10)
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
    status = models.CharField(max_length=8,
                              choices=[('received', 'Received'), ('returned', 'Returned'), ('shipping', 'Shipping')])
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    # date = models.DateField()
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_order_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.code


class PurchaseTransaction(models.Model):
    purchase_order = models.ForeignKey(PurchaseOder, on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    quantity = models.IntegerField()
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="purchase_transation_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


def __str__(self):
    return self.purchase_order.code + " Transaction"


class SalesTransaction(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    quantity = models.IntegerField()
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_transaction_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sales_order.code + " Transaction"
