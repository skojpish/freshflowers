from django.contrib import admin
from . import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

class DisplayAdminOTW(admin.ModelAdmin):
    list_display = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

class DisplayAdminIS(admin.ModelAdmin):
    list_display = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date', 'status']
    list_edit = ['name', 'photo', 'description', 'category', 'price', 'col', 'mult', 'minimum', 'item_date']

admin.site.register(models.Item, DisplayAdminOTW)
admin.site.register(models.InStock, DisplayAdminIS)
