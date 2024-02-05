from django.contrib import admin
from . import models

class DisplayStat(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'username']

admin.site.register(models.User, DisplayStat)

class DisplayOrders(admin.ModelAdmin):
    list_display = ['user_name', 'link_user', 'order_user', 'type_of_b', 'fullname', 'number', 'time_ord']

admin.site.register(models.Order, DisplayOrders)