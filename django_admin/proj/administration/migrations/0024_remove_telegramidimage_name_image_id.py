# Generated by Django 4.2.7 on 2024-01-19 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0023_alter_telegramidimage_name_image_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramidimage',
            name='name_image_id',
        ),
    ]