from django.contrib import admin
from .models import Club, Player


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
