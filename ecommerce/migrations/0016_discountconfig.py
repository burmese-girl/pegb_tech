# Generated by Django 4.1 on 2022-09-26 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_userprofile_customer_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Customer Category', max_length=256)),
                ('amount_percent', models.IntegerField(default=0, verbose_name='Discount(%)')),
            ],
        ),
    ]