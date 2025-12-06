from django.contrib import admin
from . import models
from .inlines import ProductImageInLine
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.

class OrderItemInline(admin.TabularInline):
    min_num = 1
    max_num = 10
    model = models.OrderItem
    autocomlete_fields = ['product']

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name__istartswith']
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        url = (reverse('admin:store_orderitem_changelist')
               + '?'
               + urlencode({'order__customer__id':str(customer.id)})
               )
        return format_html('<a href = "{}">{}</a>',url,customer.orders_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    inlines = [ProductImageInLine]
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price','collection_title','inventory_status']
    list_select_related = ['collection']
    def collection_title(self,product):
        return product.collection.title
    @admin.display(ordering ='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection','last_update',InventoryFilter]
    @admin.action(description='clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.'
        )
    class Media:
        css = {
            'all':['store/styles.css']
        }
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['customer','payment_status','placed_at']

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'product', 'quantity')
    list_filter = ('order__customer',)
    @admin.display(ordering='order_id')
    def order_id(self, order_item):
        return order_item.order.id

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','products_count']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection__id':str(collection.id)})
               )
        return format_html('<a href = "{}">{}</a>',url,collection.products_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )