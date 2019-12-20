from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from .models import Order,Product,User
from libs.Alipay import get_out_trade_no, get_paymentlink

# 订单序列化
class OrderModelSerializer(ModelSerializer):
    prod_id = serializers.IntegerField(write_only=True)
    count = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order

        '''
        prods = [(1,4), (2,3)]  (商品id，count)
        '''
        fields = ['prod_id', 'count', 'order_price', 'consignee_info']

    def validate(self, attrs):
        total_price = 0
        total_amount = float(attrs.get('order_price'))
        # 获取商品id和数量，判断总价是否正确
        prod_id, count = attrs.pop('prod_id'), attrs.pop('count')
        try:
            prod_obj = Product.objects.filter(pk=prod_id).first()
            total_price += prod_obj.price * count
        except Exception as e:
            raise serializers.ValidationError('商品主键有误')
        if total_price != total_amount:
            raise serializers.ValidationError('订单总价存在问题！')

        order_on = get_out_trade_no()

        # 生成订单链接
        subject = '宠物狗'
        order_link = get_paymentlink(subject=subject, order_num=order_on, total_amount=total_amount)
        # 将支付链接保存到Serializer对象中
        self.paymentLink = order_link
        # self.paymentLink = 'sssssssss'
        # 将其他字段加入到attrs中
        attrs['order_num'] = order_on
        user = User.objects.filter(pk=1).first()
        attrs['user'] = user
        # attrs['user'] = self.context.get('request').user

        return attrs
