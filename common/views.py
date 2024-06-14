from dataclasses import dataclass, asdict
import uuid
import json
import requests
import asyncio

from redis import Redis
from django.contrib.auth.models import User
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import renderer_classes, action
from asgiref.sync import sync_to_async

from common.models import QuestRun, Quest, DialogList
from .user_serializer import UserSerializer
from .quest_serializer import QuestSerializer
from .utils import Prompt

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
    def make_prompt(self, request):
        make_public = request.data.pop("public", False)
        prompt = Prompt(**request.data)
        req_ticket = uuid.uuid4()
        new_quest = Quest(uuid=str(req_ticket), creator=request.user, public=make_public)
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

    @action(detail=True, methods=['POST'])
    def rate_quest(self, request, pk=None):
        quest = get_object_or_404(self.get_queryset(), pk=pk)
        ranking = request.data.get("ranking", None)
        if not ranking:
            raise ParseError("Missing 'ranking' key")
        quest.ranking = ranking
        quest.save()
        serializer = QuestSerializer(quest)
        return Response(serializer.data)


