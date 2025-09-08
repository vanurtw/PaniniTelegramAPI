from django.contrib import admin
from .models import TelegramUserModel, MyUserModel, UserFootballerCollection, ProfileTelegramUser, UserFriends


@admin.register(TelegramUserModel)
class TelegramUserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(MyUserModel)
class MyUserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFootballerCollection)
class UserFootballerCollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileTelegramUser)
class ProfileTelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFriends)
class UserFriendsAdmin(admin.ModelAdmin):
    pass
