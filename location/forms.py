from django import forms
from django.forms import inlineformset_factory
from location.models import Location

class LocationCreationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ('number_of_products','type','code','company', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')

    def __init__(self, *args, **kwargs):
        super(LocationCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].widget.input_type == 'checkbox':
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'
