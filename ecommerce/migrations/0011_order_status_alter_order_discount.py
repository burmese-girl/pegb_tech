# Generated by Django 4.1 on 2022-09-25 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_order_deli_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Waiting', 'Waiting'), ('Ready', 'Ready'), ('Finish', 'Finish')], default='Draft', help_text='Status', max_length=256),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, default=0, verbose_name='Discount % '),
        ),
    ]
