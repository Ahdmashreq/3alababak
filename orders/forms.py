from django import forms
from djmoney.forms import MoneyWidget

from inventory.models import Item
from orders.models import PurchaseOder
from django.forms import inlineformset_factory, modelformset_factory
from orders.models import PurchaseOder, PurchaseTransaction, SalesOrder, SalesTransaction, MaterialTransaction, \
    MaterialTransaction1, MaterialTransactionLines
from djmoney.models.fields import MoneyField
from dal import autocomplete


class PurchaseOrderCreationForm(forms.ModelForm):
    # my_global_price = forms.DecimalField(max_digits=200, decimal_places=2)
    my_total_price_after_discount = forms.DecimalField(max_digits=200, decimal_places=2)

    class Meta:
        model = PurchaseOder
        exclude = ('currency', 'balance', 'status', 'company', 'created_at', 'last_updated_at', 'created_by',
                   'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderCreationForm, self).__init__(*args, **kwargs)
        self.fields['purchase_code'].widget.attrs['readonly'] = True
        self.fields['global_price'].widget.attrs['readonly'] = True
        self.fields['global_price'].widget.attrs['disabled'] = True
        self.fields['my_total_price_after_discount'].widget.attrs['readonly'] = True
        self.fields['my_total_price_after_discount'].widget.attrs['disabled'] = True
        # amount, currency = self.fields['global_price'].fields
        # amount.widget.attrs['readonly'] = True
        # amount.widget.attrs['disabled'] = True
        # currency.widget.attrs['readonly'] = True
        # currency.widget.attrs['disabled'] = True
        # self.fields['global_price'].widget = CustomMoneyWidget(
        #      amount_widget=amount.widget, currency_widget=currency.widget)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomMoneyWidget(MoneyWidget):
    template_name = 'money.html'


class PurchaseTransactionCreationForm(forms.ModelForm):
    temp_uom = forms.CharField(max_length=30, required=False)
    # my_total_price = forms.DecimalField(max_digits=200, decimal_places=2)
    # my_price_per_unit = forms.DecimalField(max_digits=200, decimal_places=2)
    after_discount = forms.DecimalField(max_digits=200, decimal_places=2)

    class Meta:
        model = PurchaseTransaction
        exclude = ('currency', 'balance', 'status', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            # 'item': forms.Select(attrs={'onchange': 'myAction(this)'}),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:items_list",
                                              attrs={'onchange': 'myAction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseTransactionCreationForm, self).__init__(*args, **kwargs)
        # amount, currency = self.fields['total_price'].fields
        # currency.initial = 'EGP'
        # amount2, currency2 = self.fields['price_per_unit'].fields
        # currency2.initial = 'EGP'

        # amount.widget.attrs['readonly'] = True
        # amount.widget.attrs['disabled'] = True
        # currency.widget.attrs['readonly'] = True
        # currency.widget.attrs['disabled'] = True
        self.fields['temp_uom'].widget.attrs['readonly'] = True
        self.fields['price_per_unit'].widget.attrs['onchange'] = 'myFunction(this)'
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['disabled'] = True
        self.fields['after_discount'].widget.attrs['readonly'] = True
        self.fields['after_discount'].widget.attrs['disabled'] = True

        # amount2.widget.attrs['onchange'] = 'myFunction(this)'
        # self.fields['price_per_unit'].widget = CustomMoneyWidget(
        #     amount_widget=amount2.widget, currency_widget=currency2.widget)
        # self.fields['total_price'].widget = CustomMoneyWidget(
        #     amount_widget=amount.widget, currency_widget=currency.widget)

        for field in self.fields:
            if field == 'total_price':
                self.fields['total_price'].widget.attrs['class'] = 'unique-class  form-control'

            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SaleOrderCreationForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ('currency', 'company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        super(SaleOrderCreationForm, self).__init__(*args, **kwargs)
        self.fields['sale_code'].widget.attrs['readonly'] = True
        self.fields['subtotal_price'].widget.attrs['readonly'] = True
        self.fields['subtotal_price'].widget.attrs['disabled'] = True

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
        super(SaleTransactionCreationForm, self).__init__(*args, **kwargs)
        self.fields['temp_uom'].widget.attrs['readonly'] = True
        self.fields['price_per_unit'].widget.attrs['onchange'] = 'myFunction(this)'
        self.fields['location'].widget.attrs['onchange'] = 'inventory(this)'
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['disabled'] = True
        self.fields['temp_unit_cost'].widget.attrs['readonly'] = True
        self.fields['temp_unit_cost'].widget.attrs['disabled'] = True

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
        exclude = ('transaction_type', 'stoke_take', 'sale_order', 'created_at', 'last_updated_at',
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
        super(MaterialTransactionLinesCreationForm, self).__init__(*args, **kwargs)
        po_transactions = PurchaseTransaction.objects.select_related('item').filter(purchase_order__id=id,
                                                                                    status='open')
        print("Hiiiiiiiiiiiiii", po_transactions)
        items = Item.objects.filter(name__in=list(po_transactions))
        print(items)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['item'].queryset = items


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
