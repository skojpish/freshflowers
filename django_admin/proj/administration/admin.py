from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

class DisplayAdminOTW(admin.ModelAdmin):
    list_display = ['name', 'get_html_photo_otw', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

    def get_html_photo_otw(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=70>")

    get_html_photo_otw.short_description = "Фото"

admin.site.register(models.Item, DisplayAdminOTW)

class DisplayAdminIS(admin.ModelAdmin):
    list_display = ['name', 'get_html_photo_inst', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

    def get_html_photo_inst(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=70>")

    get_html_photo_inst.short_description = "Фото"

admin.site.register(models.InStock, DisplayAdminIS)
