from django.contrib import admin
from account.models import *

# Register your models here.
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(Attendance_Interface)


class AddressInline(admin.TabularInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,

    ]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,

    ]
