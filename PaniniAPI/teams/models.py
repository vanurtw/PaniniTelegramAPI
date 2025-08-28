from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.services import upload_photo_player


class Club(models.Model):
    '''
    Футбольный клуб
    '''
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100
    )
    founded = models.IntegerField(
        verbose_name='Год основания',
        validators=[MinValueValidator(1500)]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Футбольный клуб'
        verbose_name_plural = 'Футбольные клубы'


class Player(models.Model):
    '''
    Футболист
    '''
    CHOICES = [
        ('GK', 'Вратарь'),
        ('DF', 'Защитник'),
        ('MF', 'Полузащитник'),
        ('FW', 'Нападающий'),
    ]
    CHOICES_CARD_STATUS = [
        ('NOR', 'Обычная'),
        ('RA', 'Редкая'),
        ('LEG', 'Легендарная')
    ]
    name = models.CharField(
        verbose_name='Имя',
        max_length=100
    )
    club = models.ForeignKey(
        to=Club,
        verbose_name='Клуб',
        on_delete=models.CASCADE,
        related_name='players'
    )
    position = models.CharField(
        verbose_name='Позиция',
        max_length=2,
        choices=CHOICES
    )
    status_card = models.CharField(
        verbose_name='Статус карыты',
        max_length=3,
        choices=CHOICES_CARD_STATUS
    )
    number = models.IntegerField(
        verbose_name='Игровой номер',
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    birth_date = models.DateField('Дата рождения')

    photo = models.ImageField(
        verbose_name='Фото',
        upload_to=upload_photo_player,
        default='default.jpg'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Футболист'
        verbose_name_plural = 'Футболисты'