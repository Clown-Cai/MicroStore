from django.db import models

from product.models import Product

# 供应商表
class Supplier(models.Model):
    compony_name = models.CharField(max_length=256)
    addr = models.CharField(max_length=256)
    linkman = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    products = models.ManyToManyField(to=Product, through='Supplier2Product',
                                      through_fields=('supplier', 'product'))

    class Meta:
        db_table = 'Supplier'

    def __str__(self):
        return self.compony_name


# 供应商-商品表
class Supplier2Product(models.Model):
    supplier = models.ForeignKey(to='Supplier', db_constraint=False, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Supplier2Product'

    def __str__(self):
        return '%s' %self.id

# 库存表
class Inventory(models.Model):
    product = models.OneToOneField(to=Product, db_constraint=False, on_delete=models.CASCADE)
    inventory_num = models.IntegerField(default=0)       # 总库存数
    current_invintory = models.IntegerField(default=0)   # 现有库存数
    sale_num = models.IntegerField(default=0)            # 已售数量


# 库存变更表
class InventoryChange(models.Model):
    choices = ((1, '进货'), (0, '退货'))
    product = models.ForeignKey(to=Product, db_constraint=False, on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(to='Supplier', db_constraint=False, on_delete=models.DO_NOTHING)
    change_type = models.IntegerField(choices=choices)
    count = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'InventoryChange'

    def __str__(self):
        return '%s' %self.id
