from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from django.db.models import F
from django.db.transaction import atomic

from .models import Address, User
from .serializers import AddressModelSerializer, AddressSer


# 收货地址增删改查
class AddressListAPIView(ListAPIView):
    user = User.objects.filter(pk=1).first()
    queryset = Address.objects.filter(user=user).all()
    serializer_class = AddressModelSerializer

    # 创建收货地址
    def post(self, request):
        user = User.objects.filter(pk=1).first()
        if user.addr_num < 10:
            user_id = 1
            consignee = request.data.get('consignee')
            phone = request.data.get('phone')
            addr = request.data.get('addr')
            data = {'user':user_id, 'consignee':consignee, 'phone':phone, 'addr':addr}
            addr_serializer = AddressSer(data=data)
            if addr_serializer.is_valid():
                addr_serializer.save()
                User.objects.filter(pk=1).update(addr_num=F('addr_num')+1)
                return Response(data={'code':1, 'msg':'地址添加成功'})
            return Response(data={'code':0, 'msg':'地址添加失败'})
        else:
            return Response(data={'code':2, 'msg':'地址数不能超过10个'})


# 收货地址创建
# class AddressAPIView(APIView):
#     def post(self, request):
#         user = User.objects.filter(pk=1).first()
#         if user.addr_num < 10:
#             user_id = 1
#             consignee = request.data.get('consignee')
#             phone = request.data.get('phone')
#             addr = request.data.get('addr')
#             data = {'user':user_id, 'consignee':consignee, 'phone':phone, 'addr':addr}
#             addr_serializer = AddressSer(data=data)
#             if addr_serializer.is_valid():
#                 addr_serializer.save()
#                 return Response(data={'code':1, 'msg':'地址添加成功'})
#             return Response(data=addr_serializer.errors)
#         else:
#             return Response(data={'code':2, 'msg':'地址数不能超过10个'})




# 删除收货地址
class AddrDestroyAPIView(DestroyAPIView):
    queryset = Address.objects.filter(user_id=1).all()


# 修改收货地址默认值
class AddrDefaultAPIView(APIView):
    def patch(self, request):
        addr_id = request.data.get('addr_id')
        addr_obj = Address.objects.filter(user_id=1, is_default=True).first()
        if addr_obj:
            if addr_id == addr_obj.pk:
                return Response(data={'code':2, 'msg':'已经是默认地址了'})
            else:
                with atomic():
                    # 将默认地址改为非默认，再将前台传来的地址改为默认地址
                    Address.objects.filter(user_id=1, is_default=True).update(is_default=False)
                    Address.objects.filter(pk=addr_id).update(is_default=True)
                    return Response(data={'code':1, 'msg':'设置成功'})
        else:
            Address.objects.filter(pk=addr_id).update(is_default=True)
            return Response(data={'code': 1, 'msg': '设置成功'})



