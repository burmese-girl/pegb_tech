from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from . import models
import re
from datetime import datetime
import json
from django.contrib.auth import authenticate


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='order.customer_name', required=False, allow_blank=True)
    customer_phone = serializers.CharField(
        source='order.customer_phone', required=False, allow_blank=True)
    customer_address = serializers.CharField(
        source='order.customer_address', required=False, allow_blank=True)
    discount = serializers.DecimalField(
        source='order.discount', decimal_places=2, max_digits=20, required=False, )
    tax = serializers.DecimalField(
        source='order.tax', decimal_places=2, max_digits=20, required=False, )
    total = serializers.DecimalField(
        source='order.total', decimal_places=2, max_digits=20, required=False, )
    sub_total = serializers.DecimalField(
        source='order.sub_total', decimal_places=2, max_digits=20, required=False, )
    customer_state = serializers.CharField(
        source='order.customer_township', required=False, allow_blank=True)
    deli_fee = serializers.DecimalField(
        source='order.deli_fee', decimal_places=2, max_digits=20, required=False, )

    class Meta:
        model = models.Order
        fields = ('id', 'customer_name', 'customer_phone', 'customer_address',
                  'customer_state', 'sub_total',
                  'discount', 'tax', 'deli_fee', 'total',)

        extra_kwargs = {
            'deli_fee': {'write_only': True, 'allow_blank': True, 'required': False},
            'tax': {'write_only': True},
            'total': {'read_only': True}
        }

    def validate_customer_phone(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def create(self, validate_data):
        create_date = datetime.now()
        order = models.Order(**validate_data)
        order.create_date = create_date
        customer_data = self.initial_data.get('customer')
        customer_json = json.loads(customer_data)
        user_id = customer_json.get('customer_id')
        user = User.objects.get(id=user_id)
        profile = models.UserProfile.objects.get(user_id=user.pk)
        profile.create_from = "Web"
        profile.save()
        order.customer_id_id = user.pk
        order.customer_name = customer_json.get('name')
        order.customer_phone = customer_json.get('phone')
        order.customer_address = customer_json.get('address')
        order.customer_state = customer_json.get('township')
        order.discount = customer_json.get('discount')
        order.tax = customer_json.get('tax')
        order.sub_total = customer_json.get('sub_total')
        order.deli_fee = customer_json.get('deli_fee')
        order.total = customer_json.get('total')
        order.payment_type = customer_json.get('payment_type')
        order.banking_type = customer_json.get('banking_type') or "-"
        if customer_json.get('banking_image') != '':
            order.banking_image = customer_json.get('banking_image').split('/')[2]
        order.save()
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                    print("User Data", data["user"])
                else:
                    msg = "User is not active."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "You must provide both username and password in this login API"
            raise exceptions.ValidationError(msg)

        return data

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =models.ProductCategory
        fields = ('name','complete_name')
class AddProductSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer()
    class Meta:
        model = models.Product
        fields = ('name', 'selling_price', 'weight', 'quantity','product_category')

    # def get_product_category(self, obj):
    #     return obj.category_id.name

    def create(self, validate_data):
        product = models.Product(**validate_data)
        product.uom="kg"
        product.currency="usd"
        product.save()
        print(product.id)
        return product


class DiscountConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DiscountConfig
        fields = ('name', 'amount_percent')

    def create(self, validate_data):
        discount = models.DiscountConfig(**validate_data)
        discount.save()
        print("Discount Id :",discount.id)
        return discount

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value




