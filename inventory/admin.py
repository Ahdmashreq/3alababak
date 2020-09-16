from django.contrib import admin
from inventory.models import *
from mptt.admin import MPTTModelAdmin



# Register your models here.
# admin.site.register(product,)
admin.site.register(Brand)
#admin.site.register(Category)
admin.site.register(Uom)
# admin.site.register(item)
# admin.site.register(product_attribute)
admin.site.register(Attribute)
admin.site.register(Category, MPTTModelAdmin)

# admin.site.register(item_attribute_value)

class ItemAttributeValueInline(admin.TabularInline):
    model = ItemAttributeValue


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute


class ItemInline(admin.TabularInline):
    model = Item


class StokeEntryInline(admin.TabularInline):
    model = StokeEntry


@admin.register(StokeTake)
class StokeTake(admin.ModelAdmin):
    inlines = [
        StokeEntryInline,
    ]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [

        ItemAttributeValueInline,

    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttributeInline,
        ItemInline,

    ]
