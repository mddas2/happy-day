# Generated by Django 4.1.4 on 2023-01-09 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0005_blog_main_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='configure_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
