from .models import AnswerOption
from users.models import ProfileTelegramUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F


@receiver(post_save, sender=AnswerOption)
def create_forecast_tg_user(sender, instance, created, *args, **kwargs):
    if instance.correct:
        user_forecasts = ProfileTelegramUser.objects.filter(user_forecasts__answer_option=instance)
        user_forecasts.update(coins=F("coins") + 1000)
        print("add coins")
