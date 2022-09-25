from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
from . import forms
from . import models


class UserProfileAdmin(SimpleHistoryAdmin):
    form = forms.UserDetailAdminForm
    ordering = ['user']
    search_fields = ['user']
    list_display = ['user','customer_category' ,'gender', 'country_code',
                    'mobile', 'dob', 'active_user', 'created_from']
    search_fields = ['user','mobile', 'created_from', 'country_code']
    list_per_page = 20


class ProductCategoryAdmin(SimpleHistoryAdmin):
    list_per_page = 20
    ordering = ['id']
    search_fields = ['name']
    list_display = ['name', 'complete_name', ]


class ProductAdmin(SimpleHistoryAdmin):
    list_per_page = 20
    search_fields = ['name']
    ordering = ['name']
    list_display = ['name','selling_price','currency','uom']


class CustomerCategoryAdmin(SimpleHistoryAdmin):
    list_per_page = 20
    ordering = ['id']
    search_fields = ['name']
    list_display = ['name', 'complete_name','num_orders_from','num_orders_to']


class OrderAdmin(SimpleHistoryAdmin):
    form = forms.OrderFormAdmin
    change_form_template = "./admin/change_form.html"
    list_per_page = 20
    date_hierarchy = 'create_date'
    ordering = ['-create_date']
    exclude = ['order_quantity']
    search_fields = ['order_no', 'status', 'create_date', 'customer_name']
    list_display = ['order_no','create_date','customer_name', 'sub_total', 'tax','discount', 'deli_fee' ,'total','status']


class OrderItemAdmin(SimpleHistoryAdmin):
    list_per_page = 20
    # ordering =['-create_date']
    search_fields = ['order__order_no', 'product__name']
    list_display = ['product', 'order', 'qty', 'price']


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.CustomerCategory,CustomerCategoryAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)