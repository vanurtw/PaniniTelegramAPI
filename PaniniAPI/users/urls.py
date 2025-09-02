from rest_framework.urls import path
from .views import ProfileTelegramUser

urlpatterns = [
    path('profile/', ProfileTelegramUser.as_view()),

]
