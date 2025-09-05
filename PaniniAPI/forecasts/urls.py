from rest_framework.urls import path
from .views import ForecastsReadAPIView, UserForecastsAPIView

urlpatterns = [
    path("forecasts/", ForecastsReadAPIView.as_view()),
    path("forecasts/my/", UserForecastsAPIView.as_view()),

]
