from rest_framework.urls import path
from .views import PurchasePlayerAPIView

urlpatterns = [
    path('purchase/', PurchasePlayerAPIView.as_view()),

]
