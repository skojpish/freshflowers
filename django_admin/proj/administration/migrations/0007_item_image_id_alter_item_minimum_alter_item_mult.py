# Generated by Django 4.2.7 on 2023-12-12 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0006_item_category_item_minimum_item_mult_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_id',
            field=models.TextField(blank=True, null=True, verbose_name='image ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='minimum',
            field=models.IntegerField(blank=True, null=True, verbose_name='Минимальное количество'),
        ),
        migrations.AlterField(
            model_name='item',
            name='mult',
            field=models.IntegerField(blank=True, null=True, verbose_name='Кратность'),
        ),
    ]
