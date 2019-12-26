from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
import re
from django.core.cache import cache
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.db.models import Q

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


# 手机号码登录验证
class MobileLoginModelSerializer(ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, write_only=True)
    class Meta:
        model = User
        fileds = ['phone', 'code']


    def validate_phone(self, value):
        print(value)
        if re.match(r'^[1][34578][0-9]{9}$', value):
            return value
        raise serializers.ValidationError({'value': '手机号格式有问题'})

    def validate(self, attrs):
        code = attrs.pop('code')
        mobile = attrs.get('phone')
        if cache.get(mobile) != code:
            raise serializers.ValidationError('验证码错误')

        # 签发token
        user = User.objects.filter(phone=mobile).first()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.user = user
        self.token = token
        return attrs


class LoginModelSerializer(ModelSerializer):
    username = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        # 账号密码登录 => 多方式登录
        user = self._many_method_login(**attrs)

        # 签发token，并将user和token存放到序列化对象中
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        self.user = user
        self.token = token

        return attrs

    # 多方式登录
    def _many_method_login(self, **attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if re.match(r'^1[3-9][0-9]{9}$', username):
            user = User.objects.filter(phone=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError({'username': '账号有误'})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': '密码有误'})

        return user


# 用户注册
class RegisterModelSerializer(ModelSerializer):
    checkPass = serializers.CharField(min_length=6, max_length=16, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'checkPass', 'phone', 'email']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('checkPass'):
            raise serializers.ValidationError({'checkPass':'两次密码不一致'})

        user = User.objects.filter(Q(username=attrs.get('username')) | Q(phone=attrs.get('phone')))
        if user:
            raise serializers.ValidationError('用户已存在')
        attrs.pop('checkPass')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
