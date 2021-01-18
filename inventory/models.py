from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from unidecode import unidecode
from account.models import Company
from alababak.utils import arabic_slugify
from inventory.manager import UomCategoryManager, UomManager
from location.models import Location
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils.text import slugify as slugy

class Brand(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="brand_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            obj = Brand.objects.get(id=self.id)
            if obj.name != self.name:
                self.create_slug()
        except Brand.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(Brand, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.company.id),allow_unicode=True)


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='sub_category')
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="category_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            obj = Category.objects.get(id=self.id)
            if obj.name != self.name:
                self.create_slug()
        except Category.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.company.id),allow_unicode=True)


class UomCategory(models.Model):
    name = models.CharField(max_length=30)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="uom_category_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'company']

    def save(self, *args, **kwargs):
        try:
            obj = UomCategory.objects.get(id=self.id)
            if obj.name != self.name:
                self.create_slug()
        except UomCategory.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(UomCategory, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.company.id),allow_unicode=True)


class Uom(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=[('reference', 'Reference Unit of Measure of this category'),
                                                    ('smaller', 'Smaller Than The Reference Unit of Measure '),
                                                    ('bigger', 'Bigger Than The Reference Unit of Measure')])
    ratio = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True,
                                help_text="A content for this thing")
    category = models.ForeignKey(UomCategory, on_delete=models.CASCADE, related_name='uoms')
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="uom_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'category', 'company']

    def clean(self):
        # Don't allow two uoms in the same category to be of type 'reference'.
        if self.type == 'reference':
            uoms_with_same_category = Uom.objects.filter(company=self.company, category=self.category, type='reference')
            if len(uoms_with_same_category) != 0:
                raise ValidationError({"type": "Reference UOM for this category already exists."})

    def save(self, *args, **kwargs):

        try:
            obj = Uom.objects.get(id=self.id)
            if obj.name != self.name or obj.category != self.category:
                self.create_slug()
        except Uom.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(Uom, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.company.id), allow_unicode=True)


class Product(models.Model): 
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='product_category')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="product_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.brand.name


class Attribute(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    name = models.CharField(max_length=50)
    att_type = models.CharField(max_length=50, null=True, blank=False,
                                choices=[('text', 'text'), ('number', 'number'), ('date', 'date'),
                                         ('checkbox', 'checkbox')])
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)

    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="attribute_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            obj = Attribute.objects.get(id=self.id)
            if obj.name != self.name:
                self.create_slug()
        except Attribute.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(Attribute, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.att_type) + '-' + str(self.company.id),allow_unicode=True)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, )
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="product_attribute_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product.name + ' ' + self.attribute.name


class Item(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, )
    uom = models.ForeignKey(Uom, on_delete=models.CASCADE, blank=True, null=True, related_name='uom')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=30, blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True, unique=True)
    expirable = models.BooleanField(default=False, verbose_name='Expirable', help_text='Checkbox if item is expirable')
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="item_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['company','sku'] , name='unique_sku_with_company'),
        ]


class ItemAttributeValue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, )
    value = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="item_attribute_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item.name + ' ' + self.attribute.name


class StokeTake(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    category = TreeForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                              related_name='stoke_category')
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30,
                            choices=[('location', 'By Location'), ('category', 'By Category'),
                                     ('random', 'Random')], default='location')
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)

    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=[('Drafted', 'Drafted'), ('In Progress', 'In Progress'),
                                                      ('Pending Approval', 'Pending Approval'),
                                                      ('Approved', 'Approved'),
                                                      ('Done', 'Done')], default='Drafted')
    random_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="stoketake_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            obj = StokeTake.objects.get(id=self.id)
            if obj.name != self.name:
                self.create_slug()
        except StokeTake.DoesNotExist:
            self.create_slug()

        if not self.slug:
            self.slug = arabic_slugify(self.name)

        super(StokeTake, self).save(*args, **kwargs)

    def create_slug(self):
        self.slug = slugy(self.name + '-' + str(self.company.id),allow_unicode=True)


class StokeEntry(models.Model):
    stoke_take = models.ForeignKey(StokeTake, on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stoke_entry")
    quantity = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="stoke_entry_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item.name


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, )
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    last_updated_at = models.DateField(null=True, auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                   related_name="image_created_by")
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.item.name + ' image'