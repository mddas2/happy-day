# Generated by Django 4.1.4 on 2023-06-10 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0031_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
