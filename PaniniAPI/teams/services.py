def upload_photo_player(instance, file):
    '''
    Построение пути для загрузки фото футболистов
    '''
    return f"clubs/{instance.club}/{instance.name}/{file}"
