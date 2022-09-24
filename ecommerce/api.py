
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.db import transaction
from rest_framework import generics
from . import models
from . import serializers
import json
import scrape_helper
logger = scrape_helper.getlogger("Api")

class OrderConfirm(views.APIView):  # Submit Order Only from ajax API
    # permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()

    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    # template_name = 'order_success.html'

    def get(self, request, format=None):
        content = {'status': 'Request was permitted from GET API'}
        return Response(content)
        return Response(serializers.UserSerializer(request.user).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        transaction.atomic()
        logger.debug("[Order Submit - {0}] Data: {1}".format(
            request.query_params.get('site', ''), request.data))

        order_ser = serializers.OrderSerializer(data=request.data)
        if not order_ser.is_valid():
            logger.warn("[{0}]invalid Order, rollback - {1}".format(
                request.data.get('customer', ''), order_ser.errors))

            transaction.rollback()
            return Response(order_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        order_ser.save()
        order = models.Order.objects.get(id=order_ser.data['id'])
        order.save()
        products = request.data['product_list']
        json_data = json.loads(products)
        for prod in json_data:
            product_raw = str(json_data[prod]).replace(" ", "")
            product_json = json.loads(product_raw)
            discount_price = 0.00
            order_qty = int(product_json['qty'])
            price = int(product_json['price'].replace(
                '\n', '').replace(',', ''))
            product = models.Product.objects.get(id=int(prod))
            orderItem, created = models.OrderItem.objects.get_or_create(order_id=order.pk,
                                                                        product_id=product.pk,
                                                                        qty=order_qty, price=price)
            update_items = {'order': orderItem.order.id, 'product': orderItem.product.id, 'price': orderItem.price,
                            'qty': orderItem.qty, 'discount_price': discount_price}
            orderitem_ser = serializers.OrderItemSerializer(
                orderItem, data=update_items)
            if not orderitem_ser.is_valid():
                logger.warn(
                    "[{0}] invalid orderitem, rollback - {1}".format(request.data.get('customer', ''),
                                                                     orderitem_ser.errors))

                transaction.rollback()
                return Response(orderitem_ser.errors, status=status.HTTP_400_BAD_REQUEST)
            orderitem_ser.save()
        transaction.commit()

        logger.debug("[*** Order Success - {0}] ***".format(order))
        print("**** serializers.OrderSerializer(order).data ",
              serializers.OrderSerializer(order).data)
        customer_data = request.data.get('customer')
        customer_json = json.loads(customer_data)
        customer_name = customer_json.get('name')
        customer_phone = customer_json.get('phone')
        customer_address = customer_json.get('address')
        customer_township = customer_json.get('township')
        discount = customer_json.get('discount')
        tax = customer_json.get('tax')
        sub_total = customer_json.get('sub_total')
        deli_fee = customer_json.get('deli_fee')
        total = customer_json.get('total')

        content_order = {'order_no': str(order.order_no), 'total': str(total), 'tax': str(tax), 'discount': str(discount), 'deli_fee': str(deli_fee),
                         'sub_total': str(sub_total), 'customer_name': order.customer_name, 'customer_phone': order.customer_phone,
                         'customer_township': customer_township, 'customer_address': customer_address, 'payment_type': order.payment_type, 'banking_type': order.banking_type}

        return Response(content_order, status=status.HTTP_201_CREATED)