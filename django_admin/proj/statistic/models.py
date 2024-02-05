from django.db import models

class User(models.Model):
    user_id = models.IntegerField(verbose_name="User Id")
    username = models.CharField(verbose_name="Username")

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

class Order(models.Model):
    user_name = models.CharField(verbose_name="Пользователь", max_length=100)
    link_user = models.CharField(verbose_name="Ссылка", max_length=100, blank=True, null=True)
    order_user = models.TextField(verbose_name="Состав заказа")
    type_of_b = models.CharField(verbose_name="Тип бизнеса", max_length=100)
    fullname = models.CharField(verbose_name="ФИО", max_length=100)
    number = models.CharField(verbose_name="Номер телефона", max_length=100)
    time_ord = models.DateTimeField(verbose_name="Время заявки", null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'