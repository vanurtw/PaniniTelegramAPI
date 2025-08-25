from rest_framework.urls import path
from .views import TelegramAuthView

urlpatterns = [
    path('auth/login/', TelegramAuthView.as_view()),
]
