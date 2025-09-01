from django.contrib import admin
from .models import Club, Player


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
