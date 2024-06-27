from dataclasses import dataclass, asdict
import uuid
import json
import requests
import asyncio

from redis import Redis
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import renderer_classes, action
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import QuestRun, Quest, DialogList, QuestRating
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH
from common.serializers import QuestSerializer, UserSerializer
from common.quest_prompt_generator import Prompt, QuestPrompt

r = Redis(host='127.0.0.1', port=6379, decode_responses=True)

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = User.objects.order_by("-id")
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]

    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        data = request.data
        if not data.get("username") or not data.get("password"):
            raise ParseError("Missing details")
        found_user = authenticate(username=data.get("username"), password= data.get("password"))
        if not found_user:
            raise ParseError("Invalid details")
        new_tokens = RefreshToken.for_user(found_user)
        return Response({"access": str(new_tokens.access_token), "refresh": str(new_tokens)})
    
    @action(detail=False, methods=['POST'])
    def make_prompt(self, request):
        make_public = request.data.pop("public", False)
        prompt = Prompt(**request.data)
        req_ticket = uuid.uuid4()
        new_quest = Quest(uuid=str(req_ticket), creator=request.user, public=make_public, rating=0.0)
        new_quest.save()
        prompt.queue_generation(str(req_ticket))
        return Response({"ticket": req_ticket})

    # @action(detail=False, methods=['PUT'])
    # def poll_prompt(self, request): # maybe I just need to run this all under the job.. then send out a FB message to let the user know they can get their new quest.
    #     ticket = request.data.get("ticket")
    #     found_res = r.get(ticket)
    #     found_quest = Quest.objects.filter(uuid=ticket).first() # for now lets just assume this will be ok
    #     if found_res:
    #         url_list = json.loads(found_res)
    #         idx = 0
    #         for filename in url_list:
    #             url = filename.replace(STATIC_MUSIC_PATH,STATIC_HOSTNAME)
    #             new_dialog = DialogList(quest=found_quest, index=idx, url=url)
    #             new_dialog.save()
    #             idx = idx + 1
    #         r.delete(ticket)
    #         return Response({"ready": True, "response": [fb.url for fb in found_quest.dialogs.order_by("index")]})
    #     return Response({"ready": False, "response": []})


    
class QuestViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = Quest.objects.order_by("-id")
    serializer_class = QuestSerializer
    renderer_classes = [JSONRenderer]

    
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
    def personal_quests(self, request):
        public_queryset = self.get_queryset().filter(creator=request.user)
        serializer = QuestSerializer(public_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def rate_quest(self, request):
        quest = Quest.objects.filter(id=request.data.get("pk")).first()
        if not quest:
            raise ParseError("Quest not found")
        ranking = request.data.get("ranking", None)
        if not ranking:
            raise ParseError("Missing 'ranking' key")
        new_rating = QuestRating(rating=ranking, quest=quest)
        new_rating.save()
        # quest.rating = ranking
        # quest.save()
        serializer = QuestSerializer(quest)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def quest_prompts(self, request):
        return Response({"prompts": QuestPrompt.song_type_map.keys()})


