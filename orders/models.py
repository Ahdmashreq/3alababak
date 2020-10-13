from django.db import models
from djmoney.models.fields import MoneyField
from account.models import Supplier, Customer, Company
from inventory.models import Item
from django.conf import settings
from moneyed import Money, EGP
from currencies.models import Currency
from inventory.models import StokeTake
from location.models import Location


# import django_filters


# Create your models here.
class PurchaseOder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, )
    order_name = models.CharField(max_length=10)
    purchase_code = models.CharField(max_length=100, help_text='code number of a po',null=True, blank=True, )
    global_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    status = models.CharField(max_length=20,
                              choices=[('drafted', 'Drafted'), ('Partial_receive', 'Partially Received'),
                                       ('closed', 'Closed'), ('open', 'Open')], default='open')
    date = models.DateField(null=True, blank=True)
    balance = models.IntegerField(help_text='The remaining quantities to be received', default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    discount_type = models.CharField(max_length=11,
                                     choices=[('percentage', '%'), ('amount', 'EGP')], default='percentage')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="purchase_order_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order_name

    @property
    def global_price_after_discount(self):
        if self.discount_type == 'percentage':
            discount_amount = self.global_price / 100 * self.discount
            return round(self.global_price - discount_amount, 2)
        elif self.discount_type == 'amount':
            return round(self.global_price - self.discount, 2)


class SalesOrder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    order_name = models.CharField(max_length=10)
    sale_code = models.CharField(max_length=100, help_text='code number of a so',null=True, blank=True, )
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    status = models.CharField(max_length=8,
                              choices=[('received', 'Received'), ('returned', 'Returned'), ('shipping', 'Shipping')],
                              default='drafted')
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_order_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order_name


class PurchaseTransaction(models.Model):
    purchase_order = models.ForeignKey(PurchaseOder, on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(max_length=8,
                              choices=[('closed', 'Closed'), ('open', 'Open')], default='open')
    created_at = models.DateField(auto_now_add=True, null=True)
    balance = models.IntegerField(help_text='The remaining quantities to be received for this item',
                                  blank=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="purchase_transation_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.item)

    @property
    def total_price_after_discount(self):
        discount_amount = self.total_price / 100 * self.discount_percentage
        return round(self.total_price - discount_amount, 2)


class SalesTransaction(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    quantity = models.IntegerField()
    price_per_unit = MoneyField(max_digits=14, decimal_places=2, null=True, blank=True, default_currency='EGP')
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_transaction_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sales_order.code + " Transaction"


# class PoFilter(django_filters.FilterSet):
#     class Meta:
#         model = PurchaseTransaction
#         fields = ['item']

class MaterialTransaction1(models.Model):
    transaction_code = models.CharField(max_length=100, help_text='code number of a transaction')
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, blank=True, null=True)
    purchase_order = models.ForeignKey(PurchaseOder, on_delete=models.CASCADE, blank=True, null=True)
    stoke_take = models.ForeignKey(StokeTake, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="transaction1_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                        related_name="transaction1_last_updated_by")

    def __str__(self):
        return self.transaction_code


class MaterialTransactionLines(models.Model):
    material_transaction = models.ForeignKey(MaterialTransaction1, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    transaction_type = models.CharField(max_length=4,
                                        choices=[('in', 'in'), ('out', 'out')])
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="line_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                        related_name="line_last_updated_by")

    def __str__(self):
        return self.item.name


class MaterialTransaction(models.Model):
    transaction_code = models.CharField(max_length=100, help_text='code number of a transaction')
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, blank=True, null=True)
    purchase_order = models.ForeignKey(PurchaseOder, on_delete=models.CASCADE, blank=True, null=True)
    stoke_take = models.ForeignKey(StokeTake, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    transaction_type = models.CharField(max_length=4,
                                        choices=[('in', 'in'), ('out', 'out')])
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="transaction_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                        related_name="transaction_last_updated_by")

    def __str__(self):
        return self.transaction_code
