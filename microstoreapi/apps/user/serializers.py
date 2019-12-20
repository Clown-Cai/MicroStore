from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import re

from .models import Address, User


class AddressModelSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'addr', 'consignee', 'phone']


class AddressSer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr', 'consignee', 'phone', 'user']
        extra_kwargs = {
            'user': {
                'write_only': True,
            }
        }

    def validate_phone(self, value):
        print(value)
        if re.match(r'^[1][34578][0-9]{9}$', value):
            return value
        raise serializers.ValidationError({'value': '手机号格式有问题'})
