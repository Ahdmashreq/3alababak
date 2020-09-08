from django import forms
from djmoney.forms import MoneyWidget

from orders.models import PurchaseOder
from django.forms import inlineformset_factory
from orders.models import PurchaseOder, PurchaseTransaction, SalesOrder, SalesTransaction
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
    uom_dummy = forms.CharField(max_length=30)
    unit_price_dummy = forms.DecimalField(max_digits=2)
    class Meta:
        model = PurchaseOder
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')
        widgets = {
            #'item': forms.Select(attrs={'onchange': 'myAction(this)'}),
            'quantity': forms.TextInput(attrs={'onchange': 'myFunction(this)'}),
            'item': autocomplete.ModelSelect2(url="orders:items_list",attrs={'onchange': 'myAction(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseTransactionCreationForm, self).__init__(*args, **kwargs)
        amount, currency = self.fields['total_price'].fields
        self.fields['total_price'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget)
        self.fields['uom_dummy'].disabled = True
        self.fields['unit_price_dummy'].disabled = True
        self.fields['total_price'].disabled = True


        for field in self.fields:
            if field == 'total_price':
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
        for field in self.fields:
            if field == 'total_price':
                self.fields[field].widget.attrs['class'] = 'form-control'

            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SaleTransactionCreationForm(forms.ModelForm):
    class Meta:
        model = SalesTransaction
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(SaleTransactionCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'total_price':
                self.fields[field].widget.attrs['class'] = 'form-control'

            elif self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


purchase_transaction_formset = inlineformset_factory(PurchaseOder, PurchaseTransaction,
                                                     form=PurchaseTransactionCreationForm, extra=4, can_delete=True)

sale_transaction_formset = inlineformset_factory(SalesOrder, SalesTransaction,
                                                 form=SaleTransactionCreationForm, extra=3, can_delete=True)
