# Generated by Django 3.1.1 on 2021-08-12 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cart_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='cart',
        ),
    ]
