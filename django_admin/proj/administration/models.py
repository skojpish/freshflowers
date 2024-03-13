from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import format_html

# Create your models here.

class Item(models.Model):
    objects = models.Manager()

    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    photo = models.ImageField(verbose_name="Фото", upload_to="items/", blank=True)
    description = models.CharField(verbose_name="Описание", max_length=100)
    category = models.CharField(verbose_name="Категория", max_length=50)
    price = models.FloatField(verbose_name="Цена")
    col = models.IntegerField(verbose_name="Количество")
    mult = models.IntegerField(verbose_name="Кратность", blank=True, null=True)
    minimum = models.IntegerField(verbose_name="Мин. кол.", blank=True, null=True)
    item_date = models.DateField(verbose_name="Дата прибытия")
    image_id = models.CharField(verbose_name="image ID", blank=True, null=True, editable=False)
    name_image_id = models.CharField(verbose_name="name image ID", blank=True, null=True, editable=False)

    def status(self):
        if self.photo == '' and self.image_id is None:
            return format_html(
                '<span style="color: red;">{} {}</span>',
                'Нет',
                'фото'
            )
        else:
            return format_html(
                '<span style="color: green;">{} {}</span>',
                'Фото',
                'есть'
            )


    class Meta:
        verbose_name = 'Товар в пути'
        verbose_name_plural = 'Товары в пути'

class InStock(models.Model):
    objects = models.Manager()

    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    photo = models.ImageField(verbose_name="Фото", upload_to="items/", blank=True)
    description = models.CharField(verbose_name="Описание", max_length=100)
    category = models.CharField(verbose_name="Категория", max_length=50)
    price = models.FloatField(verbose_name="Цена")
    col = models.IntegerField(verbose_name="Количество")
    mult = models.IntegerField(verbose_name="Кратность", blank=True, null=True)
    minimum = models.IntegerField(verbose_name="Мин. кол.", blank=True, null=True)
    item_date = models.DateField(verbose_name="Прибыл")
    image_id = models.CharField(verbose_name="image ID", blank=True, null=True, editable=False)
    name_image_id = models.CharField(verbose_name="name image ID", blank=True, null=True, editable=False)

    def status(self):
        if self.photo == '' and self.image_id is None:
            return format_html(
                '<span style="color: red;">{} {}</span>',
                'Нет',
                'фото'
            )
        else:
            return format_html(
                '<span style="color: green;">{} {}</span>',
                'Фото',
                'есть'
            )

    class Meta:
        verbose_name = 'Товар в наличии'
        verbose_name_plural = 'Товары в наличии'

class TelegramIdImage(models.Model):
    objects = models.Manager()

    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    id_image = models.CharField(verbose_name="Id фото в телеге", unique=True)

class ExcelInput(models.Model):
    excel_file = models.FileField(upload_to="excel/", validators=[FileExtensionValidator(['xlsx', 'xls'])])

class PriceList(models.Model):
    price_list = models.FileField(upload_to="pricelist/")

    class Meta:
        verbose_name = 'Прайс лист'
        verbose_name_plural = 'Прайс лист'

class Mailing(models.Model):
    objects = models.Manager()

    mail_text = models.TextField(verbose_name="Текст рассылки")
    date_time = models.DateTimeField(verbose_name="Дата и время публикации")
    status_new = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name = 'Рассылку'
        verbose_name_plural = 'Рассылки'
