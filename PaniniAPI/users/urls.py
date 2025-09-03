from rest_framework.urls import path
from .views import ProfileTelegramUser, FarmStartUserAPIView, FarmEndUserAPIView, FarmAPIView

urlpatterns = [
    path('profile/', ProfileTelegramUser.as_view()),
    path('farm/', FarmAPIView.as_view()),
    path('farm/start/', FarmStartUserAPIView.as_view()),
    path('farm/collect/', FarmEndUserAPIView.as_view())

]
