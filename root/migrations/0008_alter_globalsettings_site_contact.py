# Generated by Django 4.1.4 on 2023-01-22 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0007_globalsettings_tiktok_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsettings',
            name='site_contact',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
