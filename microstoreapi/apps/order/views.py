from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from django.db.transaction import atomic

from .models import ProductCollection, ShoppingCart, OrderInfo, Order
from product.models import Product
from user.models import User
from .serializers import OrderModelSerializer
from libs.Alipay import alipay

# Create your views here.
class ProductCollectionAPIView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.filter(pk=product_id).first()
        user = User.objects.filter(pk=1).first()  # 先默认一个用户
        # user = request.user
        # 查看用户是否已经收藏
        collection = ProductCollection.objects.filter(product=product, user=user).first()
        if collection:
            return Response(data={'code':2, 'msg':'已经收藏过了'})
        # 创建一条收藏记录
        row = ProductCollection.objects.create(product=product, user=user)
        print(row)
        if row:
            return Response(data={'code':1, 'msg':'添加收藏成功'})
        else:
            return Response(data={'code':0, 'msg':'添加收藏失败'})


# 加入购物车
class ShoppingAPIView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        product_num = request.data.get('num')
        if type(product_num) is int and product_num <= 0:
            product_num = 1
        product = Product.objects.filter(pk=product_id).first()
        user = User.objects.filter(pk=1).first()
        # 判断购物车中是否有该商品
        shop = ShoppingCart.objects.filter(product=product, user=user)
        if shop:
            shop.update(count=F('count') + product_num)
        else:
            row = ShoppingCart.objects.create(product=product, user=user, count=product_num)
            if not row:
                return Response(data={'code': 0, 'msg': '添加购物车失败'})
        return Response(data={'code': 1, 'msg': '添加购物车成功'})


# 订单
class OrderAPIView(APIView):

    def post(self, request):
        # 获取订单中商品信息
        prod_id = request.data.get('prod_id')
        count = request.data.get('count')
        serializer = OrderModelSerializer(data=request.data, context={'request': request})
        # 信息校验
        serializer.is_valid(raise_exception=True)
        with atomic():
            # 订单入库
            order = serializer.save()
            # 订单详情入库
            obj = Product.objects.filter(pk=prod_id).first()
            OrderInfo.objects.create(
                product=obj,
                unit_price=obj.price,
                count=count,
                order=order
            )
        # 返回一个支付链接
        return Response(serializer.paymentLink)

# 支付成功后，支付宝返回给后台
class SuccessAPIView(APIView):
    def post(self, request):
        data = request.data
        signature = data.pop('sign')
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            order = Order.objects.filter(order_num=data.get('out_trade_no'))
            if order.first().pay_status != 1:
                order.update(pay_status=1)
                return Response('success')
            print("trade succeed")
        return Response('failed')