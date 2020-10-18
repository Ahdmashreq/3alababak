from django.contrib import admin
from orders.models import *

# Register your models here.

class PurchaseTransactionInline(admin.TabularInline):
    model = PurchaseTransaction


class MaterialTransactionLinesInline(admin.TabularInline):
    model = MaterialTransactionLines


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

@admin.register(MaterialTransaction1)
class MaterialTransaction1Admin(admin.ModelAdmin):
    model = MaterialTransaction1
    inlines = [
        MaterialTransactionLinesInline,
    ]
