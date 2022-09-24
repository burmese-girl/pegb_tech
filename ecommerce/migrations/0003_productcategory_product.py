# Generated by Django 4.1 on 2022-09-24 05:55

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_userprofile_email_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name', max_length=256)),
                ('complete_name', models.CharField(blank=True, help_text='Complete Name', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Product Name', max_length=255)),
                ('selling_price', models.IntegerField(blank=True, help_text='Price')),
                ('product_image', models.ImageField(blank=True, default='placeholder.png', help_text='Product Image', null=True, storage=django.core.files.storage.FileSystemStorage(location='ecommerce/static/login/images/upload/'), upload_to='products')),
                ('currency', models.CharField(blank=True, default='Ks', help_text='Currency', max_length=255)),
                ('is_sale', models.BooleanField(default=True, help_text='Available in Sale')),
                ('barcode', models.CharField(blank=True, help_text='Barcode', max_length=12)),
                ('details', models.TextField(blank=True, default='Product exports from China with High Quality. We always use the fresh and good quality.', verbose_name='Product Detail')),
                ('weight', models.FloatField(blank=True, default=1, verbose_name='Product Weight')),
                ('uom', models.CharField(blank=True, default='kg', max_length=10, verbose_name='Unit of Measurement')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('cart_quantity', models.IntegerField(default=1, verbose_name='Cart Quantity')),
                ('order_quantity', models.IntegerField(default=1, verbose_name='Order Quantity')),
                ('category_id', models.ForeignKey(default=1, help_text='Product Category', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productcategory')),
            ],
        ),
    ]
