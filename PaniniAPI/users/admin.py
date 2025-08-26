from django.contrib import admin
from .models import TelegramUserModel, MyUserModel


@admin.register(TelegramUserModel)
class TelegramUserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(MyUserModel)
class MyUserModelAdmin(admin.ModelAdmin):
    pass
