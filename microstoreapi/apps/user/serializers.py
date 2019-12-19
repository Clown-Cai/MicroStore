from rest_framework.serializers import ModelSerializer

from .models import Address, User

class AddressModelSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr', 'consignee', 'phone']


class AddressSer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['addr', 'consignee', 'phone']

        def validate(self,attrs):
            user = User.objects.filter(pk=1).first()
            attrs['user_id'] = user.pk
            print(attrs)
            return attrs