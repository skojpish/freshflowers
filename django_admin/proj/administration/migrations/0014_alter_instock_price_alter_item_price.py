# Generated by Django 4.2.7 on 2024-01-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0013_alter_instock_options_alter_item_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instock',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
    ]
