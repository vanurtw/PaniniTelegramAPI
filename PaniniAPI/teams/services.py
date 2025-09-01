from django.utils.text import slugify
from transliterate import slugify


def upload_photo_player(instance, file):
    '''
    Построение пути для загрузки фото футболистов
    '''
    club_name = instance.club.name
    club_slug = slugify(club_name)
    if not club_slug:
        club_slug = club_name
    filename, typ = file.split('.')
    filename_slug = slugify(filename)
    if not filename_slug:
        filename_slug = filename
    return f"clubs/{club_slug}/{filename_slug}.{typ}"
