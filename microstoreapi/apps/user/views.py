from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Address, User
from .serializers import AddressModelSerializer, AddressSer


# 收货地址查询
class AddressListAPIView(ListAPIView):
    user = User.objects.filter(pk=1).first()
    queryset = Address.objects.filter(user=user).all()
    serializer_class = AddressModelSerializer


# 收货地址创建
class AddressAPIView(CreateAPIView):
    serializer_class = AddressSer
