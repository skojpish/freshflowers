from django.db import models

class User(models.Model):
    user_id = models.IntegerField(verbose_name="User Id")
    username = models.CharField(verbose_name="Username")

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
