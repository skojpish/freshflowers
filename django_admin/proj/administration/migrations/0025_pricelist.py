# Generated by Django 4.2.7 on 2024-01-29 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0024_remove_telegramidimage_name_image_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_list', models.FileField(upload_to='pricelist/')),
            ],
        ),
    ]
