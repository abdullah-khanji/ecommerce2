# Generated by Django 3.1 on 2020-08-25 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='store',
            field=models.CharField(default='', max_length=200),
        ),
    ]
