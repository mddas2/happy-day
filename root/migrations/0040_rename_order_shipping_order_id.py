# Generated by Django 4.1.4 on 2023-06-11 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0039_alter_shipping_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipping',
            old_name='order',
            new_name='order_id',
        ),
    ]
