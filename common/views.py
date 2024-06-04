from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, action
import requests
import json
from common.models import Run
from django.contrib.auth.models import User
from .user_serializer import UserSerializer
from .run_serializer import RunSerializer

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = User.objects.order_by("-id")
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]

    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def make_prompt(self, request):
        print(request.user)
        prompt = request.data.get("prompt", "hello")
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        res = requests.post('http://localhost:11434/api/generate', data=json.dumps(data))
        res_json = res.json()
        # TODO: Maybe have a server complete the command and insert into redis under a key to later obtain by mobile
        return Response({"message": res_json["response"]})


class RunViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "put", "delete"]
    queryset = Run.objects.order_by("-id")
    serializer_class = RunSerializer
    renderer_classes = [JSONRenderer]

    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = RunSerializer(user, context={'request': request})
        return Response(serializer.data)

