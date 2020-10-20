from rest_framework import serializers
from inventory.models import Attribute


class AttributeSeializer(serializers.ModelSerializer):
    att_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = Attribute
        fields = ('att_type',)
