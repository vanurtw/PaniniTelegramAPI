from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ClubSerializer, PlayerSerializer
from rest_framework.response import Response
from .models import Player, Club


class CollectionsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    def get(self, request):
        data = Player.objects.all()
        print(data[0].photo.url)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)
