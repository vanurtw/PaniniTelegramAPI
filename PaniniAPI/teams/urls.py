from django.urls import path
from .views import CollectionsAPIView, FootballClubAPIView

urlpatterns = [
    path('collections/<slug:slug>/', CollectionsAPIView.as_view()),
    path('football-clubs/', FootballClubAPIView.as_view())
]
