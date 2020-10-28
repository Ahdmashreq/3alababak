from rest_framework import serializers
from account.models import Customer, Supplier


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'landline', 'status')


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'landline', 'status')
