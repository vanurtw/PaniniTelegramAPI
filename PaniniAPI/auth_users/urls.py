from rest_framework.urls import path
from .views import TelegramAuthView, TestAPIVIew

urlpatterns = [
    path('auth/login/', TelegramAuthView.as_view()),

    path('auth/test/', TestAPIVIew.as_view())
]
