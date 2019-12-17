from django.db import models



# 商品表
class Product(models.Model):
    name = models.CharField(max_length=256)
    describe = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    market_price = models.DecimalField(max_digits=7, decimal_places=2)  # 市场价
    img = models.ImageField(upload_to='media/img_prod/')
    is_unshelve = models.BooleanField(default=0)   # 是否下架
    repertory = models.IntegerField()    # 库存数
    sale_num = models.IntegerField()    # 销量
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category', db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Product'

    def __str__(self):
        return self.name


# 商品类型
class Category(models.Model):
    name = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.name









