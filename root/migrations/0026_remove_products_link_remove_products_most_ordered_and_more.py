# Generated by Django 4.1.4 on 2023-05-06 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0025_membershiptype_code_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='link',
        ),
        migrations.RemoveField(
            model_name='products',
            name='most_ordered',
        ),
        migrations.RemoveField(
            model_name='products',
            name='most_viewed',
        ),
    ]
