from django.utils.text import slugify
from transliterate import slugify


def upload_photo_player(instance, file):
    '''
    Построение пути для загрузки фото футболистов
    '''

    club_slug = slugify(instance.club.name)
    player_slug = slugify(instance.name)
    filename, typ = file.split('.')
    return f"clubs/{club_slug}/{player_slug}/{slugify(filename)}.{typ}"
