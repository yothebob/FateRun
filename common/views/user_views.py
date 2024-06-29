from dataclasses import dataclass, asdict
import uuid

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

from common.models import Quest, DialogList, QuestRun, Tag
from common.serializers import UserSerializer
from common.quest_prompt_generator import Prompt

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
        found_tag = Tag.objects.filter(prompt=request.data.get("setting")).first()
        if not found_tag:
            raise ParseError("Prompt setting not supported")
        new_quest = Quest(uuid=str(req_ticket),
                          creator=request.user,
                          public=make_public,
                          rating=0.0,
                          tags=found_tag,
                          prompt=prompt.generate_prompt()) # todo: extract genre from setting
        new_quest.save()
        prompt.queue_generation(str(req_ticket))
        return Response({"ticket": req_ticket})

    @action(detail=False, methods=['POST'])
    def complete_quest(self, request):
        data = request.data
        new_run = QuestRun(**data)
        new_run.save()
        return Response({"created": True})

