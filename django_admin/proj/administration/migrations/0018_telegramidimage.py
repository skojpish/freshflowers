# Generated by Django 4.2.7 on 2024-01-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0017_alter_instock_name_alter_item_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramIdImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('id_image', models.CharField(max_length=100, unique=True, verbose_name='Id фото в телеге')),
            ],
        ),
    ]