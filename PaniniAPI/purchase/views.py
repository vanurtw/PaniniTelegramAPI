from teams.models import Player
from users.models import UserFootballerCollection
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import ProfileTelegramUser
from django.db.models import F, Q
from rest_framework import status
from teams.models import Player
from random import choices, choice
from teams.serializers import PlayerSerializer


class PurchasePlayerAPIView(GenericAPIView):
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''
        Покупка карточки футболиста за игровые очки(монеты)
        Списываем монеты у пользователя, если недостаточно, то отменяем операцию и возвращаем ошибку
        Выбираем произвольную карточку футболиста и записываем его в коллекцию пользователя
        Возращаем данные выбранного футболиста
        '''
        update = (ProfileTelegramUser.objects
                  .filter(telegram_user=request.user, coins__gte=100)
                  .update(coins=F('coins') - 100))
        if not update:
            return Response({"detail": "Not enough coins"}, status=status.HTTP_400_BAD_REQUEST)
        user_players = request.user.profile.footballer_cards.all()
        players = Player.objects.filter(~Q(id__in=user_players.values('player_id')))
        if not players:
            return Response({"detail": "The collection of football players is empty"})
        player = choice(players)
        try:
            UserFootballerCollection.objects.create(telegram_user=request.user.profile, player=player)
        except Exception as ex:
            return Response(ex)
        serializer = self.serializer_class(player, many=False, context={'tg_user_players': [player.id]})

        return Response(serializer.data)
