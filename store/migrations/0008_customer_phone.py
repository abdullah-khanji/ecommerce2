# Generated by Django 3.1 on 2020-08-25 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_orderitem_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
