
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from . import models
import re
from datetime import datetime
import json
from django.contrib.auth import authenticate


class OrderSerializer(serializers.ModelSerializer):
    # order_no = serializers.CharField(source='order.order_no', required=False, allow_blank=True)
    customer_name = serializers.CharField(
        source='order.customer_name', required=False, allow_blank=True)
    customer_phone = serializers.CharField(
        source='order.customer_phone', required=False, allow_blank=True)
    customer_address = serializers.CharField(
        source='order.customer_address', required=False, allow_blank=True)
    # sale_person = serializers.CharField(source='order.sale_person', required=False, allow_blank=True)
    # create_date = serializers.DateTimeField(source='order.create_date', required=False,)
    discount = serializers.DecimalField(
        source='order.discount', decimal_places=2, max_digits=20, required=False, )
    tax = serializers.DecimalField(
        source='order.tax', decimal_places=2, max_digits=20, required=False, )
    total = serializers.DecimalField(
        source='order.total', decimal_places=2, max_digits=20, required=False, )
    sub_total = serializers.DecimalField(
        source='order.sub_total', decimal_places=2, max_digits=20, required=False, )
    # order_quantity = serializers.IntegerField(source='order.order_quantity', required=False,)
    customer_township = serializers.CharField(
        source='order.customer_township', required=False, allow_blank=True)
    # delivery = serializers.CharField(source='order.delivery', required=False, allow_blank=True)
    deli_fee = serializers.DecimalField(
        source='order.deli_fee', decimal_places=2, max_digits=20, required=False, )

    class Meta:
        model = models.Order
        fields = ('id', 'customer_name', 'customer_phone', 'customer_address',
                  'customer_township', 'sub_total',
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

    def create(self, validated_data):
        user = User.objects.get(username='admin')
        # deli = models.DeliveryManagement.objects.filter(
        #     status__icontains='Draft')[0]
        create_date = datetime.now()
        order = models.Order(**validated_data)
        order.create_date = create_date
        order.sale_person_id = user.pk
        order.customer_id_id = 1 #need to put dynamic customer id
        customer_data = self.initial_data.get('customer')
        customer_json = json.loads(customer_data)
        order.customer_name = customer_json.get('name')
        order.customer_phone = customer_json.get('phone')
        order.customer_address = customer_json.get('address')
        order.customer_township = customer_json.get('township')
        order.discount = customer_json.get('discount')
        order.tax = customer_json.get('tax')
        order.sub_total = customer_json.get('sub_total')
        order.deli_fee = customer_json.get('deli_fee')
        order.total = customer_json.get('total')
        order.payment_type = customer_json.get('payment_type')
        order.banking_type = customer_json.get('banking_type') or "-"
        if customer_json.get('banking_image') != '':
            order.banking_image = customer_json.get(
                'banking_image').split('/')[2]
        print("banking image :::::::", order.banking_image)
        # if self.initial_data:
        #     # check mandatory in Order item
        #     if 'name' not in self.initial_data.get('product_list'):
        #         raise serializers.ValidationError({"customer name": ["This field is required."]})
        #
        #     if 'deli_fee' not in self.initial_data.get('product_list'):
        #         raise serializers.ValidationError({"deli_fee": ["This field is required."]})

        # self.initial_data.pop('product')

        order.save()
        return order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'