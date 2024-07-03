from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import renderer_classes, action

from common.models import Quest
from common.serializers import QuestSerializer, QuestListSerializer

    
class QuestViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = Quest.objects.order_by("-id")
    serializer_class = QuestSerializer
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if self.action == "list":
            return QuestListSerializer
        else:
            return QuestSerializer

    
    def retrieve(self, request, pk=None):
        quest = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = QuestSerializer(quest, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def public_quests(self, request):
        public_queryset = self.get_queryset().filter(public=True)
        serializer = QuestSerializer(public_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def highest_rated_quests(self, request):
        high_rated_queryset = self.get_queryset().filter(public=True).order_by("-rating")
        serializer = QuestSerializer(high_rated_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def quests_by_genre(self, request):
        genre = request.query_params.get("genre", "medieval")
        public_queryset = self.get_queryset().filter(public=True, genre=genre)
        serializer = QuestSerializer(public_queryset, many=True)
        return Response(serializer.data)

    # fix this
    # @action(detail=False, methods=['PUT'])
    # def rate_quest(self, request):
    #     quest = Quest.objects.filter(id=request.data.get("pk")).first()
    #     if not quest:
    #         raise ParseError("Quest not found")
    #     ranking = request.data.get("ranking", None)
    #     if not ranking:
    #         raise ParseError("Missing 'ranking' key")
    #     # new_rating = QuestRating(rating=ranking, quest=quest)
    #     # new_rating.save()
    #     # quest.rating = ranking
    #     # quest.save()
    #     serializer = QuestSerializer(quest)
    #     return Response(serializer.data)

    # fix this 
    # @action(detail=False, methods=['GET'])
    # def quest_prompts(self, request):
    #     return Response({"prompts": QuestPrompt.song_type_map.keys()})


