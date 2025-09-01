from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ClubSerializer, PlayerSerializer
from rest_framework.response import Response
from .models import Player, Club
from users.models import UserFootballerCollection


class CollectionsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    def get(self, request, slug):
        players = Player.objects.filter(club__slug=slug)
        tg_user_players = request.user.profile.footballer_cards.all().values_list('player_id', flat=True)
        serializer = self.serializer_class(players, many=True, context={'tg_user_players': tg_user_players})
        return Response(serializer.data)
