# Generated by Django 3.1 on 2020-08-24 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200824_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='totalPrice',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
