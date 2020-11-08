from rest_framework import serializers
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        exclude = ('created_at', 'created_by', 'last_updated_at', 'last_updated_by', 'company')
        read_only_fields = ('slug', 'code')
