from django.db import models

from user.models import User
from product.models import Product

# 订单表
class Order(models.Model):
    order_num = models.CharField(max_length=16)   # 订单号
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)  # 订单总价
    consignee_info = models.CharField(max_length=256)       # 收货人信息
    order_choices = ((0, '作废订单'), (1, '已完成订单'), (2, '活动订单'))
    order_status = models.IntegerField(choices=order_choices, default=2)
    pay_choices = ((0, '未付款'), (1, '已付款'))
    pay_status = models.IntegerField(choices=pay_choices, default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return self.order_num


# 订单详情表
class OrderInfo(models.Model):
    order = models.ForeignKey(to='Order', db_constraint=False, on_delete=models.CASCADE)
    product = models.OneToOneField(to=Product, db_constraint=False, on_delete=models.CASCADE)
    count = models.IntegerField()  # 商品数
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = ((0, '未发货'), (1, '已发货'))
    status = models.IntegerField(choices=status_choices, default=0)

    class Meta:
        db_table = 'OrderInfo'

    def __str__(self):
        return '%s' %self.id


# 浏览记录表
class BrowserHistory(models.Model):
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.CASCADE)
    browser_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BrowserHistory'

    def __str__(self):
        return '%s' %self.id


# 购物车
class ShoppingCart(models.Model):
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.CASCADE)
    count = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'ShoppingCart'

    def __str__(self):
        return '%s' %self.id


# 商品收藏表
class ProductCollection(models.Model):
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=0)
    collect_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ProductCollection'

    def __str__(self):
        return '%s' %self.id


# 销量表
class Sales(models.Model):
    product = models.OneToOneField(to=Product, db_constraint=False, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    sals_price = models.DecimalField(max_digits=12, decimal_places=2)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Sales'

    def __str__(self):
        return '%s' %self.id


# 商品评论表
class Comments(models.Model):
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, db_constraint=False, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'

    def __str__(self):
        return '%s' %self.id



