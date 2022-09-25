
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
        print("validate data in serializer::: ",customer_json.get('customer_id'))
        user_id=customer_json.get('customer_id')
        user = User.objects.get(id=user_id)
        profile = models.UserProfile.objects.get(user_id=user.pk)
        profile.create_from ="Web"
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
            order.banking_image = customer_json.get(
                'banking_image').split('/')[2]
        print("banking image :::::::", order.banking_image)

        order.save()
        return order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'