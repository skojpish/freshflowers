# Generated by Django 4.2.7 on 2024-01-19 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0022_alter_telegramidimage_name_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramidimage',
            name='name_image_id',
            field=models.CharField(null=True, verbose_name='name image ID'),
        ),
    ]
