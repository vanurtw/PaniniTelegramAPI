from django.urls import path
from .views import CollectionsAPIView

urlpatterns = [
    path('collections/', CollectionsAPIView.as_view()),
]
