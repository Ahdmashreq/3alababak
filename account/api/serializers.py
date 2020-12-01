from rest_framework import serializers
from account.models import Customer, Supplier, Address


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Address
        fields = ('id', 'address', 'country', 'city', 'phone_number', 'landline', 'zip_code')


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = ('slug', 'first_name', 'last_name', 'email', 'phone_number', 'landline', 'status', 'address')
        read_only_fields = ('slug',)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        customer = Customer.objects.create(**validated_data)
        for address in address_data:
            Address.objects.create(customer=customer, created_by=self.context['request'].user
                                   , **address)
        return customer

    def update(self, instance, validated_data, *args, **kwargs):
        try:
            address_data = validated_data.pop('address')
        except KeyError:
            address_data =[]
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.landline = validated_data.get('landline', instance.landline)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        keep_addresses = []
        for address in address_data:
            if "id" in address.keys():
                if Address.objects.filter(id=address["id"]).exists():
                    ad = Address.objects.get(id=address["id"])
                    ad.address = address.get("address", ad.address)
                    ad.country = address.get("country", ad.country)
                    ad.city = address.get("city", ad.city)
                    ad.phone_number = address.get("phone_number", ad.phone_number)
                    ad.landline = address.get("landline", ad.landline)
                    ad.zip_code = address.get("zip_code", ad.zip_code)
                    ad.last_updated_by = self.context['request'].user
                    ad.save()
                    keep_addresses.append(ad.id)
                else:
                    # if the send id doesn't exist in db, it will be ignored
                    continue
            else:
                new_ad = Address.objects.create(**address, customer=instance,
                                                created_by=self.context['request'].user)
                keep_addresses.append(new_ad.id)
        related_address = Address.objects.filter(customer=instance)
        for address in related_address:
            if address.id not in keep_addresses:
                address.delete()

        return instance


class SupplierSerializer(serializers.ModelSerializer):
    supp_address = AddressSerializer(many=True)

    class Meta:
        model = Supplier
        fields = ('slug', 'first_name', 'last_name', 'email', 'phone_number', 'landline', 'status', 'supp_address')
        read_only_fields = ('slug',)

    def create(self, validated_data):
        address_data = validated_data.pop('supp_address')
        supplier = Supplier.objects.create(**validated_data)
        for address in address_data:
            Address.objects.create(supplier=supplier, created_by=self.context['request'].user
                                   , **address)
        return supplier

    def update(self, instance, validated_data):
        try:
            address_data = validated_data.pop('supp_address')
        except KeyError:
            address_data = []
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.landline = validated_data.get('landline', instance.landline)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        keep_addresses = []
        for address in address_data:
            if "id" in address.keys():
                if Address.objects.filter(id=address["id"]).exists():
                    ad = Address.objects.get(id=address["id"])
                    ad.address = address.get("address", ad.address)
                    ad.country = address.get("country", ad.country)
                    ad.city = address.get("city", ad.city)
                    ad.phone_number = address.get("phone_number", ad.phone_number)
                    ad.landline = address.get("landline", ad.landline)
                    ad.zip_code = address.get("zip_code", ad.zip_code)
                    ad.last_updated_by = self.context['request'].user
                    ad.save()
                    keep_addresses.append(ad.id)
                else:
                    # if the send id doesn't exist in db, it will be ignored
                    continue
            else:
                new_ad = Address.objects.create(**address, supplier=instance, created_by=self.context['request'].user)
                keep_addresses.append(new_ad.id)
        related_address = Address.objects.filter(supplier=instance)
        for address in related_address:
            if address.id not in keep_addresses:
                address.delete()
        return instance
