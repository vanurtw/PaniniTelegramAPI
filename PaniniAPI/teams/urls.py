from django.urls import path
from .views import CollectionsAPIView

urlpatterns = [
    path('collections/<slug:slug>/', CollectionsAPIView.as_view()),
]
