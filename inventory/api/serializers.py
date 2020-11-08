from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from inventory.models import UomCategory, Uom, Category, Brand, Attribute


class UomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)

    def validate(self, data):
        if data.get("type", None) == 'smaller' or data.get("type", None) == 'bigger':
            if "ratio" not in data.keys():
                raise serializers.ValidationError({"ratio": "This field should be specified."})
        elif data.get("type", None) == "reference":
            uoms = Uom.objects.filter(category=data.get("category", None), type='reference')
            if len(uoms) > 0:
                raise serializers.ValidationError({"type": "Reference UOM for this category already exists."})

        return data


class UomCategorySerializer(serializers.ModelSerializer):
    uoms = UomSerializer(many=True, required=False)

    class Meta:
        model = UomCategory
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'id',)


class CategorySerializer(serializers.ModelSerializer):
    # children = serializers.PrimaryKeyRelatedField(read_only=True,source='sub_category')
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'parent', 'sub_category', ]
        read_only_fields = ('slug', 'id',)


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
