from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TelegramUserModel, ProfileTelegramUser


@receiver(post_save, sender=TelegramUserModel)
def create_profile_telegram_user(sender, instance, created, *args, **kwargs):
    ProfileTelegramUser.objects.create(telegram_user=instance)
