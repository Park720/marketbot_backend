from django.db import models

# 상품 모델델

class Product(models.Model):
    product_name = models.CharField(max_length=200,null=True, blank=True)
    sale_price = models.IntegerField(null=True, blank=True)
    stock_quantity = models.IntegerField(null=True, blank=True)
    category_code = models.CharField(max_length=100, default="UNDEFINED")
    product_description = models.TextField(null=True, blank=True)
    product_condition = models.CharField(max_length=100, null=True, blank=True)
    add_attributes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_name or "(이름 없음)"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    main_image_url = models.ImageField(upload_to='product_images/')
    sub_image_url = models.ImageField(upload_to='product_images/', null=True, blank=True)


class ProductOption(models.Model):
    product = models.ForeignKey(Product, related_name="options", on_delete=models.CASCADE)
    option_type = models.CharField(max_length=100, null=True, blank=True)
    option_value = models.CharField(max_length=100, null=True, blank=True)


class ShippingInfo(models.Model):
    product = models.ForeignKey(Product, related_name="shipping", on_delete=models.CASCADE)
    method = models.CharField(max_length=100, null=True, blank=True)
    fee = models.IntegerField()
    condition = models.CharField(max_length=200, null=True, blank=True)


class PromotionInfo(models.Model):
    product = models.ForeignKey(Product, related_name="promotions", on_delete=models.CASCADE)
    promo_title = models.CharField(max_length=100)
    promo_details = models.TextField(blank=True)

# 주문 모델

class Order(models.Model):

    ORDER_STATUS_CHOICES = [
    ('PENDING', '결제 대기 중'),
    ('PAID', '결제 완료'),
    ('IN_DELIVERY', '배송 중'),
    ('DELIVERED', '배송 완료'),
    ('CANCELLED', '주문 취소'),
    ('REFUNDED', '환불 완료'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    pay_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    buyer_name = models.CharField(max_length=100, null=True, blank=True)
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.receiver_name}님의 주문 ({self.order_date.strftime('%Y-%m-%d')})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    order_product_id = models.CharField(max_length=100)
    order_product_name = models.CharField(max_length=200)
    order_quantity = models.PositiveIntegerField()


class Delivery(models.Model):
    order = models.OneToOneField(Order, related_name="delivery", on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    delivery_company = models.CharField(max_length=100, null=True, blank=True)