from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from inventory.models import UomCategory, Uom, Category, Brand, Attribute, StokeTake, StokeEntry
from location.models import Location


class UomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)

    def validate(self, data):
        category = data.get("category", None)
        request = self.context.get("request", None)
        if request is not None and category is not None:
            company = request.user.company
            if company != category.company:
                raise serializers.ValidationError({"category": "Category does not exist."})
            elif data.get("type", None) == "reference":
                uoms = Uom.objects.filter(category=data.get("category", None), type='reference')
                if len(uoms) > 0:
                    raise serializers.ValidationError({"type": "Reference UOM for this category already exists."})
        if data.get("type", None) == 'smaller' or data.get("type", None) == 'bigger':
            if "ratio" not in data.keys():
                raise serializers.ValidationError({"ratio": "This field should be specified."})

        return data


class UomCategorySerializer(serializers.ModelSerializer):
    # uoms = UomSerializer(many=True, required=False)

    class Meta:
        model = UomCategory
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)


class CategorySerializer(serializers.ModelSerializer):
    # children = serializers.PrimaryKeyRelatedField(read_only=True,source='sub_category')
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # TODO sub category needs validation on company
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'parent', 'sub_category', ]
        read_only_fields = ('slug', 'id',)

    def get_fields(self, *args, **kwargs):
        fields = super(CategorySerializer, self).get_fields(*args, **kwargs)
        fields['parent'].queryset = Category.objects.filter(company=self.context['request'].user.company)
        #fields['sub_category'].queryset = Category.objects.filter(company=self.context['request'].user.company)
        return fields


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)


class StokeTakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StokeTake
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)

    def get_fields(self, *args, **kwargs):
        fields = super(StokeTakeSerializer, self).get_fields(*args, **kwargs)
        fields['category'].queryset = Category.objects.filter(company=self.context['request'].user.company)
        fields['location'].queryset = Location.objects.filter(company=self.context['request'].user.company)
        return fields

class StokeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StokeEntry
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by',)
        read_only_fields = ('slug', 'id', 'item', 'stoke_take',)
