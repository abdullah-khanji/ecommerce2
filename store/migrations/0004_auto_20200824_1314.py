# Generated by Django 3.1 on 2020-08-24 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.CharField(max_length=200),
        ),
    ]