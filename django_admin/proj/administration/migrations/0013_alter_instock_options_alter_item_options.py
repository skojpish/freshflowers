# Generated by Django 4.2.7 on 2023-12-29 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0012_instock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instock',
            options={'verbose_name': 'Товары в наличии', 'verbose_name_plural': 'Товары в наличии'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Товар в пути', 'verbose_name_plural': 'Товар в пути'},
        ),
    ]