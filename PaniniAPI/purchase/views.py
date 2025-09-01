from teams.models import Player
from users.models import UserFootballerCollection
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class PurchasePlayerAPIView(GenericAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("a")
