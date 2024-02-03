# Generated by Django 4.2.7 on 2024-01-17 14:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0014_alter_instock_price_alter_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(upload_to='excel/', validators=[django.core.validators.FileExtensionValidator(['xlsx'])])),
            ],
        ),
        migrations.AlterField(
            model_name='instock',
            name='photo',
            field=models.ImageField(blank=True, upload_to='items/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, upload_to='items/', verbose_name='Фото'),
        ),
    ]
