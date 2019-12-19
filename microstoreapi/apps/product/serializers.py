from rest_framework.serializers import ModelSerializer

from .models import Product, Category

# 商品序列化
class ProductModelSerializer(ModelSerializer):

    class Meta:
       model = Product
       fields = ['id', 'name', 'describe', 'price', 'market_price', 'img', 'repertory', 'sale_num', 'category_name']


class CategoryModelSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']