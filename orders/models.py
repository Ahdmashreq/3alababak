from django.db import models
from djmoney.models.fields import MoneyField
from account.models import Supplier, Customer, Company
from inventory.models import Item
from django.conf import settings
from moneyed import Money, EGP
from currencies.models import Currency


# import django_filters


# Create your models here.
class PurchaseOder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, )
    order_name = models.CharField(max_length=10)
    global_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    status = models.CharField(max_length=8,
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
            return round(self.global_price - discount_amount,2)
        elif self.discount_type == 'amount':
            return round(self.global_price - self.discount,2)


class SalesOrder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    order_name = models.CharField(max_length=10)
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='EGP')
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
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True,default='EGP' )
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(max_length=8,
                              choices=[('closed', 'Closed'), ('open', 'Open')], default='open')
    created_at = models.DateField(auto_now_add=True, null=True)
    balance = models.IntegerField(help_text='The remaining quantities to be received for this item', default=0,
                                  blank=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="purchase_transation_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.item

    @property
    def total_price_after_discount(self):
        discount_amount = self.total_price / 100 * self.discount_percentage
        return round(self.total_price - discount_amount,2)


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

class ReceivingTransaction(models.Model):
    po_transaction = models.ForeignKey(PurchaseTransaction, on_delete=models.CASCADE, )
    purchase_order = models.ForeignKey(PurchaseOder, on_delete=models.CASCADE, )
    date = models.DateField(null=True, blank=True)
    received_quantity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="receiving_transaction_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.po_transaction


class PoReceiving(models.Model):
    receiving_transaction = models.ForeignKey(ReceivingTransaction, on_delete=models.CASCADE, )
    po_transaction = models.ForeignKey(PurchaseTransaction, on_delete=models.CASCADE, )
