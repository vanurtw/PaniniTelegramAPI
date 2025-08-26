from django.db import models
from rest_framework.authtoken.models import Token

import binascii
import os
from django.utils.translation import gettext_lazy as _
from users.models import TelegramUserModel


class Token(models.Model):
    """
    Модель токена авторизации по умолчанию.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user_telegram = models.OneToOneField(
        TelegramUserModel, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("Пользователь телеграм")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Токен")
        verbose_name_plural = _("Токены")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
