# Generated by Django 4.1.4 on 2023-05-04 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0022_products_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberShipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('discount', models.IntegerField(default=True, null=True)),
                ('is_shipping_free', models.BooleanField(default=False)),
                ('discount_shipping_apply', models.BooleanField(default=False)),
            ],
        ),
    ]
