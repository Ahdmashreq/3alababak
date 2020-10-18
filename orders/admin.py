from django.contrib import admin
from orders.models import *

# Register your models here.

class PurchaseTransactionInline(admin.TabularInline):
    model = PurchaseTransaction

@admin.register(PurchaseOder)
class PurchaseOrderAdmin(admin.ModelAdmin):

    inlines = [
        PurchaseTransactionInline,
    ]

class SalesTransactionInline(admin.TabularInline):
    model = SalesTransaction


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):

    inlines = [
        SalesTransactionInline,


    ]

@admin.register(Inventory_Balance)
class Inventory_Balance_Admin(admin.ModelAdmin):
    model = Inventory_Balance
