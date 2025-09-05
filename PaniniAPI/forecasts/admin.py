from django.contrib import admin
from .models import Forecasts, AnswerOption


@admin.register(Forecasts)
class ForecastsAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass
