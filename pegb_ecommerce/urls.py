"""pegb_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ecommerce import views
from ecommerce import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('user/', include('ecommerce.urls')),
    path('product-categ/<int:pk>', views.product_category, name='product-categ'),
    path('product-details/<int:pk>', views.product_details, name='product_details'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('order/', views.order, name='order'),
    path('confirmed/', views.SuccessOrderView.as_view(), name='confirmed'),
    path('api/create-order/', api.OrderConfirm.as_view(), name='create-order'),

]
