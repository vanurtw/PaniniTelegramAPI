from django.contrib import admin
from .models import Forecasts, AnswerOption


class ForecastInline(admin.TabularInline):
    model = AnswerOption
    extra = 1
    can_delete = True


@admin.register(Forecasts)
class ForecastsAdmin(admin.ModelAdmin):
    inlines = [ForecastInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass