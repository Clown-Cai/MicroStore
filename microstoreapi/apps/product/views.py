from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from .serializers import *

'''
商品查询功能 :
    1.不传参数：查询全部商品，根据销量取前8个
    2.传入参数：根据条件查询检索后的商品
'''

# 首页展示
class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.filter(is_unshelve=False).order_by('-sale_num').all()[:6]
    serializer_class = ProductModelSerializer


# 根据商品id查询
class ProductRetriveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductModelSerializer


# 类别查找
class CategoryListAPIView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = CategoryModelSerializer


# 根据名称或描述搜索商品
class ProductSearchListAPIView(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'describe']
    filter_fields = ['category']


# 根据类别查找商品
class ProductByCategoryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        # 获取数据
        prod_list = models.Product.objects.filter(category=category_id).all()
        prod_serializer = ProductModelSerializer(prod_list, many=True)
        return Response(prod_serializer.data)


# 收藏夹
class ProductCollectCreateAPIView(CreateAPIView):
    pass