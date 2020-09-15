from django import forms
from djmoney.forms import MoneyWidget

from orders.models import PurchaseOder
from django.forms import inlineformset_factory
from orders.models import PurchaseOder, PurchaseTransaction, SalesOrder, SalesTransaction, ReceivingTransaction
from djmoney.models.fields import MoneyField
from dal import autocomplete


class PurchaseOrderCreationForm(forms.ModelForm):
    class Meta:
        model = PurchaseOder
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderCreationForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['total_price'].fields
        amount.widget.attrs['readonly'] = True
        amount.disabled = True
        currency.widget.attrs['readonly'] = True
        currency.disabled = True
        self.fields['total_price'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget)
        for field in self.fields:
            if field == 'total_price':
                self.fields[field].widget.attrs['class'] = 'form-control'

            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class CustomMoneyWidget(MoneyWidget):
    template_name = 'money.html'


class PurchaseTransactionCreationForm(forms.ModelForm):
    temp_uom = forms.CharField(max_length=30, required=False)

    class Meta:
        model = PurchaseTransaction
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            # 'item': forms.Select(attrs={'onchange': 'myAction(this)'}),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:items_list",
                                              attrs={'onchange': 'myAction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseTransactionCreationForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['total_price'].fields
        amount2, currency2 = self.fields['price_per_unit'].fields
        amount.widget.attrs['readonly'] = True
        amount.disabled = True
        currency.widget.attrs['readonly'] = True
        currency.disabled = True
        self.fields['temp_uom'].widget.attrs['readonly'] = True
        amount2.widget.attrs['onchange'] = 'myFunction(this)'

        self.fields['price_per_unit'].widget = CustomMoneyWidget(
            amount_widget=amount2.widget, currency_widget=currency2.widget)
        self.fields['total_price'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget)
        # self.fields['temp_uom'].disabled = True
        # self.fields['temp_unit_price'].disabled = True
        # self.fields['total_price'].disabled = True

        for field in self.fields:
            if field == 'total_price':
                self.fields[field].fields[0].widget.attrs['class'] = 'unique-class form-control'
                self.fields[field].fields[1].widget.attrs['class'] = 'form-control'
            elif field == 'price_per_unit':
                self.fields[field].widget.attrs['class'] = 'form-control'
            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SaleOrderCreationForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control tm', 'type': 'date', })
        }

    def __init__(self, *args, **kwargs):
        super(SaleOrderCreationForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['total_price'].fields
        amount.widget.attrs['readonly'] = True
        amount.disabled = True
        currency.widget.attrs['readonly'] = True
        currency.disabled = True

        self.fields['total_price'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget)
        for field in self.fields:
            if field == 'total_price':
                self.fields[field].widget.attrs['class'] = 'form-control'

            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SaleTransactionCreationForm(forms.ModelForm):
    temp_uom = forms.CharField(max_length=30, required=False)
    temp_unit_price = forms.DecimalField(max_digits=10, required=False)

    class Meta:
        model = SalesTransaction
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            # 'item': forms.Select(attrs={'onchange': 'myAction(this)'}),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:items_list",
                                              attrs={'onchange': 'myAction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(SaleTransactionCreationForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['total_price'].fields
        amount.widget.attrs['readonly'] = True
        amount.disabled = True
        currency.widget.attrs['readonly'] = True
        currency.disabled = True
        self.fields['temp_uom'].widget.attrs['readonly'] = True
        self.fields['temp_unit_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget)
        for field in self.fields:
            if field == 'total_price':
                self.fields[field].fields[0].widget.attrs['class'] = 'unique-class form-control'
                self.fields[field].fields[1].widget.attrs['class'] = 'form-control'
            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class ReceivingTransactionCreationForm(forms.ModelForm):
    class Meta:
        model = ReceivingTransaction
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')


    def __init__(self, *args, **kwargs):
        super(ReceivingTransactionCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


purchase_transaction_formset = inlineformset_factory(PurchaseOder, PurchaseTransaction,
                                                     form=PurchaseTransactionCreationForm, extra=0, can_delete=True)

sale_transaction_formset = inlineformset_factory(SalesOrder, SalesTransaction,
                                                 form=SaleTransactionCreationForm, extra=0, can_delete=True)

ReceivingTransactionCreation_formset = inlineformset_factory(PurchaseTransaction, ReceivingTransaction,
                                                             form=ReceivingTransactionCreationForm, extra=0,
                                                             can_delete=True)
