# Generated by Django 4.1 on 2022-09-24 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_remove_customercategory_num_orders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercategory',
            name='complete_name',
            field=models.CharField(blank=True, help_text='Category Name', max_length=256),
        ),
        migrations.AlterField(
            model_name='customercategory',
            name='name',
            field=models.CharField(blank=True, help_text='Category', max_length=256),
        ),
    ]
