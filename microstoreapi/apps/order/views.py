from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import F
from django.db.transaction import atomic
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ProductCollection, ShoppingCart, OrderInfo, Order, BrowserHistory
from product.models import Product
from user.models import User
from .serializers import OrderModelSerializer, HistoryModelSerializer, CollectionModelSerializer, \
    OrderModelSerializer, OrderInfoSerializer, ShoppingCartModelSerializer
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
            return Response(data={'code': 2, 'msg': '已经收藏过了'})
        # 创建一条收藏记录
        row = ProductCollection.objects.create(product=product, user=user)
        print(row)
        if row:
            return Response(data={'code': 1, 'msg': '添加收藏成功'})
        else:
            return Response(data={'code': 0, 'msg': '添加收藏失败'})

    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        collects = ProductCollection.objects.filter(is_delete=False, user=user).all()
        serializer = CollectionModelSerializer(collects, many=True, context={'request': request})
        return Response(serializer.data)


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

    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        products = ShoppingCart.objects.filter(user=user).all()
        serializer = ShoppingCartModelSerializer(products, many=True, context={'request':request})
        return Response(serializer.data)

    def delete(self, request):
        cart_pk = request.data.get('cart_id')
        print(cart_pk, type(cart_pk))
        if not cart_pk:
            return Response(data={'code':0, 'msg':'删除出错'})
        if type(cart_pk) is list:
            for pk in cart_pk:
                ShoppingCart.objects.filter(pk=pk).delete()
        else:
            ShoppingCart.objects.filter(pk=cart_pk).delete()
        return Response(data={'code':1, 'msg':'删除成功'})



# 订单
class OrderAPIView(APIView):

    def post(self, request):
        # 获取订单中商品信息
        prods = request.data.get('prods')
        print(prods)
        serializer = OrderModelSerializer(data=request.data, context={'request': request})
        # 信息校验
        serializer.is_valid(raise_exception=True)
        for prod_id, count in prods:
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


# 用户浏览记录的查询
class BrowserHistoryAPIView(APIView):
    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        history_list = BrowserHistory.objects.filter(user=user).all()
        serializer = HistoryModelSerializer(history_list, many=True, context={'request': request})
        return Response(serializer.data)

    def delete(self, request):
        user_id = request.data.get('user_id')
        prod_id = request.data.get('prod_id')
        BrowserHistory.objects.filter(user=user_id, product=prod_id).delete()
        return Response(data={
            'code':1,
            'msg':'删除成功'
        })



# 未支付订单
class NoPayOrderAPIView(APIView):
    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        order_list = OrderInfo.objects.filter(order__user=user, order__pay_status=0, order__order_status=2).all()
        serializer = OrderInfoSerializer(order_list, many=True, context={'request': request})
        return Response(serializer.data)


# 未发货订单
class UndeliverOrderAPIView(APIView):
    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        order_list = OrderInfo.objects.filter(order__user=user, order__pay_status=1, order__order_status=2).all()
        serializer = OrderInfoSerializer(order_list, many=True, context={'request': request})
        return Response(serializer.data)


# 待收货
class UnreceivedAPIView(APIView):
    def get(self, request):
        # user = request.user
        user = User.objects.filter(pk=1).first()
        order_list = OrderInfo.objects.filter(order__user=user, order__pay_status=1, order__order_status=2,
                                              status=1).all()
        serializer = OrderInfoSerializer(order_list, many=True, context={'request':request})
        return Response(data=serializer.data)
