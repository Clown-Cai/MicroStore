from django.conf.urls import url

from .views import *

urlpatterns = [
    url('products/$', ProductListAPIView.as_view()),
    url('detail/(?P<pk>\d+)$', ProductRetriveAPIView.as_view()),   # 根据商品id查询
    url('categories/$', CategoryListAPIView.as_view()),
    # 模糊查找，条件：[商品名，描述信息]
    url('search/$', ProductSearchListAPIView.as_view()),
    # 根据商品类别查找商品
    url('products/(?P<category_id>\d+)$', ProductByCategoryListAPIView.as_view()),
    # 使用过滤器查询
    # url('products/(?P<category_id>\d+)$', ProductByCategoryListAPIView.as_view()),


]
