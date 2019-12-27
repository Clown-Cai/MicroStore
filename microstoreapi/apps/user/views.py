from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from django.db.models import F
from django.db.transaction import atomic

from .models import Address, User
from .serializers import AddressModelSerializer, AddressSer, MobileLoginModelSerializer, \
    LoginModelSerializer, RegisterModelSerializer, UserInfoSerializer, PasswordSerializer, AvatarSerializer
from libs.tx_sms import send_sms


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


# 检查手机号是否存在
class CheckMobileAPIView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        user_obj = User.objects.filter(phone=mobile).first()
        if user_obj:
            return Response(data={'code':1, 'msg':'用户存在'})
        else:
            return Response(data={'code':0, 'msg':'用户不存在'})

# 发送验证码
class SendSMSAPIView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        flag = send_sms(mobile)
        if flag:
            return Response(data={'code':1, 'msg':'发送成功'})
        return Response(data={'code':1, '.msg':'发送失败'})


# 手机号码登录
class MobileLoginAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = MobileLoginModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # token = serializer.token
        return Response(data={
            'username':serializer.user.username,
            'token':serializer.token
        })


# 用户名、手机号码登录
class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginModelSerializer(data=data)
        if serializer.is_valid():
            return Response(data={
                'username': serializer.user.username,
                'token': serializer.token
            })
        return Response(data=serializer.errors)


# 用户注册
class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(data={'code':1,'msg':'注册成功'})


# 用户更新
class UserInfoChangeAPIView(APIView):
    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        serializer = UserInfoSerializer(user, context={'request':request})
        return Response(serializer.data)

    def patch(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        serializer = UserInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user,validated_data=request.data)
        return Response(data={'code':1,'msg':'修改成功'})


class PasswordChangeAPIView(APIView):
    def patch(self, request):
        # user = request.user
        # user = User.objects.filter(pk=1).first()
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={'code': 1, 'msg': '修改成功'})


# 头像修改
class AvatarAPIView(APIView):
    def post(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        avatar = request.data
        serialzer = AvatarSerializer(data=avatar)
        serialzer.is_valid(raise_exception=True)
        serialzer.update(instance=user,validated_data=avatar)
        return Response(data={'code':1, 'msg':'修改成功'})
