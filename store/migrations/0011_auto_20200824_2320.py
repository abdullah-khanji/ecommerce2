# Generated by Django 3.1 on 2020-08-25 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20200824_2319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='phone',
            new_name='phoneNum',
        ),
    ]
