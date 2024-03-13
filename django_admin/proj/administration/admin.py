from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from . import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

class DisplayAdminOTW(admin.ModelAdmin):
    list_display = ['name', 'get_html_photo_otw', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

    def get_html_photo_otw(self, objects):
        if objects.photo:
            return mark_safe(f"<img src='{objects.photo.url}' width=70>")

    get_html_photo_otw.short_description = "Фото"

admin.site.register(models.Item, DisplayAdminOTW)

class DisplayAdminIS(admin.ModelAdmin):
    list_display = ['name', 'get_html_photo_inst', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

    def get_html_photo_inst(self, objects):
        if objects.photo:
            return mark_safe(f"<img src='{objects.photo.url}' width=70>")

    get_html_photo_inst.short_description = "Фото"

admin.site.register(models.InStock, DisplayAdminIS)

class DisplayPriceList(admin.ModelAdmin):
    list_display = ['price_list']
    list_edit = ['price_list']

admin.site.register(models.PriceList, DisplayPriceList)

class DisplayMailing(admin.ModelAdmin):
    list_display = ['mail_text', 'date_time', 'status_date']
    list_edit = ['mail_text', 'date_time']

    def status_date(self, objects):
        if objects.date_time < timezone.now():
            return format_html(
                '<span style="color: grey;">{} {}</span>',
                'Отправлено', ''
            )
        else:
            return format_html(
                '<span style="color: green;">{} {}</span>',
                'Запланировано', ''
            )

    status_date.short_description = "Статус"

admin.site.register(models.Mailing, DisplayMailing)
