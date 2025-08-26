from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


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
    Модель пользователя телеграмм аккаунта
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

    class Meta:
        verbose_name = 'Модель пользователя телеграмм аккаунта'
        verbose_name_plural = 'Модели пользователя телеграмм аккаунта'


class MyUserModel(AbstractUser):
    '''
    Модель пользователя
    '''
    username = None
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
