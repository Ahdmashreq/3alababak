from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal
from djmoney.models.fields import MoneyField
from account.models import Supplier, Customer, Company
from inventory.models import Item
from django.conf import settings
from moneyed import Money, EGP
from currencies.models import Currency
from inventory.models import StokeTake
from location.models import Location
from decimal import Decimal


# import django_filters


# Create your models here.
class PurchaseOder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, )
    order_name = models.CharField(max_length=250)
    purchase_code = models.CharField(max_length=100, help_text='code number of a po', null=True, blank=True, )
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
    sale_code = models.CharField(max_length=100, help_text='code number of a so', null=True, blank=True, )
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    # status = models.CharField(max_length=8,
    #                           choices=[('received', 'Received'), ('returned', 'Returned'), ('shipping', 'Shipping')],
    #                           default='drafted')
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_order_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order_name

    @property
    def global_price(self):
        tax_percentage = Decimal(0.14)
        tax = tax_percentage * self.subtotal_price

        return round(self.subtotal_price - tax, 2)


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
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, default='EGP')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="sale_transaction_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.sales_order.code + " Transaction"


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


@receiver(post_save, sender=MaterialTransactionLines)
def create_or_update_inventory_balance(sender, instance, *args, **kwargs):
    if instance.material_transaction.purchase_order is not None:
        po_unit_cost = PurchaseTransaction.objects.get(purchase_order=instance.material_transaction.purchase_order)
        try:
            inventory_item_obj = Inventory_Balance.objects.get(item=instance.item, location=instance.location)
            inventory_item_obj.qnt += instance.quantity
            new_item_recieved_value = instance.quantity * po_unit_cost.price_per_unit
            inventory_item_obj.unit_cost = (inventory_item_obj.value + new_item_recieved_value) / inventory_item_obj.qnt
            new_value = inventory_item_obj.qnt * inventory_item_obj.unit_cost
            print(new_value)
            inventory_item_obj.value = new_value
            inventory_item_obj.save()
        except Inventory_Balance.DoesNotExist:
            inventory_item_obj = Inventory_Balance(
                item=instance.item,
                location=instance.location,
                unit_cost=po_unit_cost.price_per_unit,
                qnt=instance.quantity,
                value=instance.quantity * po_unit_cost.price_per_unit,
            )
            inventory_item_obj.save()

    elif instance.material_transaction.stoke_take is not None:
        inventory_item_obj = Inventory_Balance.objects.get(item=instance.item, location=instance.location)
        if instance.transaction_type == 'in':
            inventory_item_obj.qnt += instance.quantity
        elif instance.transaction_type == 'out':
            inventory_item_obj.qnt -= instance.quantity
        new_value = inventory_item_obj.qnt * inventory_item_obj.unit_cost
        inventory_item_obj.value = new_value
        inventory_item_obj.save()


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


class Inventory_Balance(models.Model):
    class Meta:
        unique_together = ['item', 'location']

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='balance')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    qnt = models.IntegerField(default=0)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="inventory_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                        related_name="inventory_last_updated_by")

    def __str__(self):
        return self.item.name + ' ' + str(self.value)

    def __unicode__(self):
        return '%s: %s' % (self.item.name, str(self.value))
