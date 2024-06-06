from dataclasses import dataclass, asdict
import uuid
import json
import requests
import asyncio

from redis import Redis
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, action
from asgiref.sync import sync_to_async

from common.models import Run
from .user_serializer import UserSerializer
from .run_serializer import RunSerializer
from .utils import Prompt

r = Redis(host='0.0.0.0', port=6379, decode_responses=True)


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
        prompt = Prompt(**request.data)
        req_ticket = uuid.uuid4()
        prompt.queue_generation(str(req_ticket))
        new_run = Run(uuid=uuid)
        new_run.save()
        request.user.user_runs.add(new_run)
        request.user.save()
        return Response({"ticket": req_ticket})

    @action(detail=False, methods=['PUT'])
    def poll_run_story(self, request):
        ticket = request.data.get("ticket")
        found_res = r.get(ticket)
        if found_res:
            r.delete(ticket)
            return Response({"ready": True, "response": list(filter(lambda i: i, found_res.split("\n")))})
        return Response({"ready": False})


    
class RunViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = Run.objects.order_by("-id")
    serializer_class = RunSerializer
    renderer_classes = [JSONRenderer]

    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = RunSerializer(user, context={'request': request})
        return Response(serializer.data)

