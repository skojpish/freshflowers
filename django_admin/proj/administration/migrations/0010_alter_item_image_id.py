# Generated by Django 4.2.7 on 2023-12-12 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0009_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image_id',
            field=models.CharField(blank=True, null=True, verbose_name='image ID'),
        ),
    ]
