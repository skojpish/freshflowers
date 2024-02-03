from django.contrib import admin
from . import models

class DisplayAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'username']

admin.site.register(models.User, DisplayAdmin)