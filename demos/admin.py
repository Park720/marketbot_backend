from django.contrib import admin

from .models import Product, ProductImage, ProductOption, ShippingInfo, PromotionInfo
from .models import Order, OrderItem, Delivery
from django.utils.html import format_html



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


class PromotionInfoInline(admin.TabularInline):
    model = PromotionInfo
    extra = 1

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'sale_price', 'stock_quantity', 'category_code')
    search_fields = ('product_name', 'category_code')
    list_filter = ('category_code',)
    inlines = [ProductImageInline, ProductOptionInline, PromotionInfoInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 0
    can_delete = False

admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_status', 'order_date', 'receiver_name', 'pay_amount')
    list_filter = ('order_status', 'order_date')
    search_fields = ('order_id', 'receiver_name')
    inlines = [OrderItemInline, DeliveryInline]

    def get_order_status_display_colored(self, obj):
        color_map = {
            'PENDING': 'gray',
            'PAID': 'blue',
            'IN_DELIVERY': 'orange',
            'DELIVERED': 'green',
            'CANCELLED': 'red',
            'REFUNDED': 'purple'
        }
        color = color_map.get(obj.order_status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_order_status_display())

    get_order_status_display_colored.short_description = "주문 상태 (컬러)"

