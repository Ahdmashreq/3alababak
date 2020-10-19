from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from inventory.models import (Category, Brand, Attribute, Uom, Item, Product, StokeTake, StokeEntry, Uom, UomCategory,
                              ItemAttributeValue)
from orders.models import Inventory_Balance
from mptt.forms import TreeNodeChoiceField


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


category_model_formset = modelformset_factory(Category, form=CategoryForm, extra=3, can_delete=False)


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


brand_model_formset = modelformset_factory(Brand, form=BrandForm, extra=3, can_delete=False)


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(AttributeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class ItemAttributeForm(forms.ModelForm):
    text_field = forms.CharField(max_length=100, required=False)
    number_field = forms.DecimalField(max_digits=200, decimal_places=2)
    date_field = forms.DateField(required=False)

    class Meta:
        model = ItemAttributeValue
        fields = '__all__'
        exclude = ('value', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(ItemAttributeForm, self).__init__(*args, **kwargs)
        self.fields['attribute'].widget.attrs['onchange'] = 'myFunction(this)'

        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


attribute_model_formset = modelformset_factory(Attribute, form=AttributeForm, extra=3, can_delete=False)
item_attribute_model_formset = inlineformset_factory(Item, ItemAttributeValue, form=ItemAttributeForm, extra=0,
                                                     can_delete=False)


class UOMForm(forms.ModelForm):
    class Meta:
        model = Uom
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'type': forms.Select(attrs={'onchange': 'myFunction()'}),
        }
        help_texts = {'ratio': "1*(this unit) = ratio * Reference unit of measurement", }

    def __init__(self, *args, **kwargs):
        super(UOMForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


uom_formset = modelformset_factory(Uom, form=UOMForm, extra=3, can_delete=False)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('product', 'company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


# product_item_inlineformset = inlineformset_factory(Product, Item, form=ItemForm, extra=3, can_delete=False)


class StokeTakeForm(forms.ModelForm):
    class Meta:
        model = StokeTake
        fields = '__all__'
        exclude = ('status', 'company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', }),
            # 'location':forms.HiddenInput(),
            'type': forms.Select(attrs={'onchange': 'myFunction()'}),
        }

    def __init__(self, *args, **kwargs):
        update = kwargs.pop('update')
        super(StokeTakeForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "(Select here)"
        self.fields['location'].empty_label = "(Select here)"

        for field in self.fields:
            if update:
                self.fields[field].disabled = True
                self.fields[field].widget.attrs['readonly'] = True

            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(StokeTakeForm, self).clean()
        item_length = len(Inventory_Balance.objects.filter(location=cleaned_data['location']))
        if cleaned_data['location'] is None:
            self.add_error('location', 'Location is required')
        else:
            item_length = len(Inventory_Balance.objects.filter(location=cleaned_data['location']))
        if cleaned_data['type'] == 'category':
            if cleaned_data['category'] is None:
                self.add_error('category', 'category is required')
        elif cleaned_data['type'] == 'random':
            if cleaned_data['random_number'] is None:
                self.add_error('random_number', 'Number of items is required')
            elif cleaned_data['random_number'] > item_length:
                self.add_error('random_number', 'Number greater than existing number of items')
        return cleaned_data


class StokeEntryForm(forms.ModelForm):
    class Meta:
        model = StokeEntry
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        approve = kwargs.pop('approve')
        super(StokeEntryForm, self).__init__(*args, **kwargs)
        self.fields['item'].disabled = True
        if approve:
            self.fields['quantity'].disabled = True

        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class UomCategoryForm(forms.ModelForm):
    class Meta:
        model = UomCategory
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(UomCategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


stoke_entry_formset = inlineformset_factory(StokeTake, StokeEntry, form=StokeEntryForm, extra=0, can_delete=False)
