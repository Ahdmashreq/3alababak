from django import forms
from account.models import Customer, Supplier, Address, Company
from django.forms import inlineformset_factory


class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'custom-switch-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class SupplierCreationForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ('company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(SupplierCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'custom-switch-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class AddressCreationForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(AddressCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'custom-switch-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(CompanyCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'


customer_address_formset = inlineformset_factory(Customer, Address, form=AddressCreationForm, extra=0, can_delete=True)
supplier_address_formset = inlineformset_factory(Supplier, Address, form=AddressCreationForm, extra=0, can_delete=True)
