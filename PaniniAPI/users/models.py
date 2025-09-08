import datetime
from datetime import time

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from teams.models import Player
from django.utils import timezone


class MyUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email обязателен")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class TelegramUserModel(models.Model):
    '''
    Модель пользователя телеграмм аккаунта - используется в app
    '''
    user_id = models.CharField(
        verbose_name='id пользователя аккаунта telegram',
        unique=True,
        max_length=12
    )
    username = models.CharField(
        verbose_name='username',
        max_length=24
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=True,
        null=True
    )
    create_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    is_authenticated = True

    def __str__(self):
        return f"TG_user_{self.username}_{self.user_id}"

    class Meta:
        verbose_name = 'Пользователя телеграмм аккаунта'
        verbose_name_plural = 'Пользователя телеграмм аккаунта'


class ProfileTelegramUser(models.Model):
    telegram_user = models.OneToOneField(
        'TelegramUserModel',
        verbose_name='Пользователь телеграм',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    coins = models.IntegerField(
        verbose_name='Монеты',
        default=0,
        validators=[MinValueValidator(0, message='Количество монет не может быть отрицательным')]
    )
    is_farm = models.BooleanField(
        verbose_name='Фарм-флаг',
        default=False
    )
    start_datatime_farm = models.DateTimeField(
        verbose_name="Время начала фарма",
        null=True,
        blank=True
    )
    end_datetime_farm = models.DateTimeField(
        verbose_name="Время окончания фарма",
        null=True,
        blank=True
    )
    time_farm = models.TimeField(
        verbose_name='Время фарма',
        default=datetime.time(hour=8),
        blank=True,
        null=True
    )

    @property
    def coins_available(self):
        '''Начисление монет по завершению фарма'''
        if not self.is_farm or not self.end_datetime_farm:
            return 0

        now = timezone.now()
        if now >= self.end_datetime_farm:
            return 1000
        print("Пытались забрать фарм!")
        return 0

    def start_farm(self):
        '''Начать фарм'''
        now = timezone.now()
        print(f"Время сервера - {now}")
        self.start_datatime_farm = now
        self.end_datetime_farm = now + timezone.timedelta(hours=self.time_farm.hour, minutes=self.time_farm.minute)
        self.is_farm = True
        self.save()

    def collect_coins(self):
        '''Закончить фарм'''
        if not self.is_farm:
            return 0

        coins_to_collected = self.coins_available
        self.coins += coins_to_collected
        self.is_farm = False
        self.start_datatime_farm = None
        self.end_datetime_farm = None
        self.save()
        return coins_to_collected

    def __str__(self):
        return f"Профиль {self.telegram_user}"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class UserFootballerCollection(models.Model):
    '''
    Коллекция футбольных карточек пользователя
    '''
    telegram_user = models.ForeignKey(
        to=ProfileTelegramUser,
        verbose_name='Профиль пользователя',
        on_delete=models.CASCADE,
        related_name='footballer_cards'
    )
    player = models.ForeignKey(
        to=Player,
        verbose_name='Футболист',
        related_name='telegram_profiles',
        on_delete=models.CASCADE
    )
    obtained_date = models.DateField(
        verbose_name='Дата получения',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.telegram_user}---{self.player}"

    class Meta:
        unique_together = ['telegram_user', 'player']
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекция'


class UserFriends(models.Model):
    user = models.ForeignKey(
        TelegramUserModel,
        on_delete=models.CASCADE,
        related_name='friends',
        verbose_name='Пользователь'
    )
    friend = models.ForeignKey(
        TelegramUserModel,
        on_delete=models.CASCADE,
        verbose_name='Друг'
    )
    create_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"{self.user} - {self.friend}"

    class Meta:
        unique_together = ['user', 'friend']
        verbose_name = 'Друзья пользоваетя'
        verbose_name_plural = 'Друзья пользоваетя'


class MyUserModel(AbstractUser):
    '''
    Модель пользователя - базовая
    '''
    username = None
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
