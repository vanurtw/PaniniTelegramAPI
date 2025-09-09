from django.db import models
from users.models import ProfileTelegramUser


class Forecasts(models.Model):
    '''
    Модель прогнозов
    '''

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255
    )
    completed = models.BooleanField(
        verbose_name='Завершен',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True
    )
    date_creation = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f"Прогноз: {self.title[:25]}..."

    class Meta:
        verbose_name = "Прогноз"
        verbose_name_plural = "Прогнозы"


class AnswerOption(models.Model):
    '''
    Модель ответов на прогнозы
    '''
    forecast = models.ForeignKey(
        Forecasts,
        on_delete=models.CASCADE,
        verbose_name='Прогноз',
        related_name='answer_options'
    )
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    correct = models.BooleanField(
        verbose_name='Верный',
        default=False
    )

    def __str__(self):
        return f"Ответ: {str(self.forecast)[:30]} - {self.title[:10]}..."

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class UserForecasts(models.Model):
    '''
    Модель ответов пользователя
    '''
    profile_user = models.ForeignKey(
        ProfileTelegramUser,
        verbose_name="Профиль пользователя",
        on_delete=models.CASCADE,
        related_name='user_forecasts'
    )
    forecast = models.ForeignKey(
        Forecasts,
        on_delete=models.CASCADE,
        verbose_name="Прогноз",
        related_name='forecasts_answer_user'
    )
    answer_option = models.ForeignKey(
        AnswerOption,
        on_delete=models.CASCADE,
        verbose_name="Вариант ответа"
    )
    date_creation = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.profile_user} - {self.forecast}"

    class Meta:
        unique_together = ['profile_user', 'forecast']
        verbose_name = "Ответ Пользователя"
        verbose_name_plural = "Ответы Пользователей"
