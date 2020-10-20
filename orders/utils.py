from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from django.forms import model_to_dict
from inventory.models import Item


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class balanceField(serializers.RelatedField):
    def to_representation(self, data):
        return model_to_dict(data)


class ItemSerializer(serializers.ModelSerializer):
    uom = serializers.StringRelatedField(many=False)
    balance = balanceField(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('uom', 'balance',)





def get_seq(n):
    if n < 1:
        return str(1).zfill(5)
    else:
        return str(n + 1).zfill(5)
