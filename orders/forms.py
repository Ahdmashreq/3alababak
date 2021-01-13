from django import forms
from django.forms import inlineformset_factory

from dal import autocomplete

from account.models import Supplier, Customer
from inventory.models import Item, Uom
from location.models import Location
from orders.models import PurchaseOder, PurchaseTransaction, SalesOrder, SalesTransaction, MaterialTransaction, \
    MaterialTransaction1, MaterialTransactionLines, Tax


class PurchaseOrderCreationForm(forms.ModelForm):
    # this field is only created for display in the form
    my_total_price_after_discount = forms.DecimalField(max_digits=200, decimal_places=2)

    class Meta:
        model = PurchaseOder
        exclude = ('currency', 'balance', 'status', 'company', 'created_at', 'last_updated_at', 'created_by',
                   'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PurchaseOrderCreationForm, self).__init__(*args, **kwargs)
        self.fields['purchase_code'].widget.attrs['readonly'] = True
        self.fields['global_price'].widget.attrs['readonly'] = True
        self.fields['global_price'].widget.attrs['disabled'] = True
        self.fields['my_total_price_after_discount'].widget.attrs['readonly'] = True
        self.fields['my_total_price_after_discount'].widget.attrs['disabled'] = True
        self.fields["supplier"].queryset = Supplier.objects.filter(company=user.company)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PurchaseTransactionCreationForm(forms.ModelForm):
    # this field is only created for display in the form
    after_discount = forms.DecimalField(max_digits=200, decimal_places=2)

    class Meta:
        model = PurchaseTransaction
        exclude = ('currency', 'balance', 'status', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:items_list",
                                              attrs={'onchange': 'myAction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PurchaseTransactionCreationForm, self).__init__(*args, **kwargs)
        # the following part is inspired from
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        # start with an empty queryset for uom field when instantiating a new form
        self.fields['uom'].queryset = Uom.objects.none()
        # get the name of item field in the instantiated form
        item_id = self['item'].auto_id
        splits = item_id.split("_")
        item_field_name = splits[1] + '_' + splits[2]
        # if item field is binded (in case of Post request),it will appear in self.data
        if item_field_name in self.data:
            try:
                item_value = int(self.data.get(item_field_name))
                item = Item.objects.get(id=item_value)
                if item is not None:
                    query = Uom.objects.filter(category=item.uom.category, company=user.company)
                else:
                    query = Uom.objects.filter(company=user.company)
                self.fields['uom'].queryset = query
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty item queryset
        elif self.instance.pk:  # in case of update request using "get" method
            self.fields['uom'].queryset = self.instance.item.uom.category.uoms
        self.fields["item"].queryset = Item.objects.filter(company=user.company)
        self.fields['price_per_unit'].widget.attrs['onchange'] = 'myFunction(this)'
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['disabled'] = True
        self.fields['after_discount'].widget.attrs['readonly'] = True
        self.fields['after_discount'].widget.attrs['disabled'] = True

        for field in self.fields:
            # setting a 'unique-class' to mark all 'total_price' fields to be used afterwards in calculating global total
            if field == 'total_price':
                self.fields['total_price'].widget.attrs['class'] = 'unique-class  form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SaleOrderCreationForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ('tax', 'currency', 'company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SaleOrderCreationForm, self).__init__(*args, **kwargs)
        self.fields['sale_code'].widget.attrs['readonly'] = True
        self.fields['subtotal_price'].widget.attrs['readonly'] = True
        self.fields['subtotal_price'].widget.attrs['disabled'] = True
        self.fields["customer"].queryset = Customer.objects.filter(company=user.company)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class SaleTransactionCreationForm(forms.ModelForm):
    temp_uom = forms.CharField(max_length=30, required=False)
    temp_unit_cost = forms.CharField(max_length=30, required=False)

    class Meta:
        model = SalesTransaction
        exclude = ('currency', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            # 'item': forms.Select(attrs={'onchange': 'myAction(this)'}),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:sell-items",
                                              attrs={'onchange': 'myAction(this)'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SaleTransactionCreationForm, self).__init__(*args, **kwargs)
        self.fields['temp_uom'].widget.attrs['readonly'] = True
        self.fields['price_per_unit'].widget.attrs['onchange'] = 'myFunction(this)'
        self.fields['location'].widget.attrs['onchange'] = 'inventory(this)'
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['disabled'] = True
        self.fields['temp_unit_cost'].widget.attrs['readonly'] = True
        self.fields['temp_unit_cost'].widget.attrs['disabled'] = True
        self.fields["location"].queryset = Location.objects.filter(company=user.company)

        for field in self.fields:
            if field == 'total_price':
                self.fields['total_price'].widget.attrs['class'] = 'unique-class  form-control'

            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class ReceivingTransactionCreationForm(forms.ModelForm):
    remaining = forms.IntegerField()

    class Meta:
        model = MaterialTransaction
        exclude = ('transaction_code', 'transaction_type', 'stoke_take', 'sale_order', 'created_at', 'last_updated_at',
                   'created_by',
                   'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', }),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id')
        super(ReceivingTransactionCreationForm, self).__init__(*args, **kwargs)
        po_transactions = PurchaseTransaction.objects.select_related('item').filter(purchase_order__id=id,
                                                                                    status='open')
        print("Hiiiiiiiiiiiiii", po_transactions)
        items = Item.objects.filter(name__in=list(po_transactions))
        print(items)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['item'].queryset = items


class MaterialTransactionCreationForm(forms.ModelForm):
    class Meta:
        model = MaterialTransaction1
        exclude = ('company', 'transaction_type', 'stoke_take', 'sale_order', 'created_at', 'last_updated_at',
                   'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', }),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialTransactionCreationForm, self).__init__(*args, **kwargs)
        self.fields['transaction_code'].widget.attrs['readonly'] = True
        # self.fields['transaction_code'].widget.attrs['disabled'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class MaterialTransactionLinesCreationForm(forms.ModelForm):
    remaining = forms.IntegerField()

    class Meta:
        model = MaterialTransactionLines
        exclude = ('transaction_type', 'created_at', 'last_updated_at', 'created_by',
                   'last_updated_by')
        widgets = {
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id')
        user = kwargs.pop('user')
        super(MaterialTransactionLinesCreationForm, self).__init__(*args, **kwargs)
        po_transactions = PurchaseTransaction.objects.select_related('item').filter(purchase_order__id=id,
                                                                                    status='open')
        items = Item.objects.filter(name__in=list(po_transactions))
        self.fields['item'].queryset = items
        self.fields['location'].queryset = Location.objects.filter(company=user.company)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = '__all__'
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(TaxForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


purchase_transaction_formset = inlineformset_factory(PurchaseOder, PurchaseTransaction,
                                                     form=PurchaseTransactionCreationForm, extra=0, can_delete=True)

sale_transaction_formset = inlineformset_factory(SalesOrder, SalesTransaction,
                                                 form=SaleTransactionCreationForm, extra=0, can_delete=True)

ReceivingTransactionCreation_formset = inlineformset_factory(PurchaseOder, MaterialTransaction,
                                                             form=ReceivingTransactionCreationForm, extra=1,
                                                             can_delete=True)

MaterialTransactionCreation_formset = inlineformset_factory(MaterialTransaction1, MaterialTransactionLines,
                                                            form=MaterialTransactionLinesCreationForm, extra=1,
                                                            can_delete=True)

# ReceivingTransactionCreation_formset = modelformset_factory(MaterialTransaction,
# form=ReceivingTransactionCreationForm, extra=1,
# can_delete=True)
