from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import renderer_classes, action

from common.models import QuestRun
from common.serializers import QuestRunSerializer

    
class QuestRunViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "head"]
    queryset = QuestRun.objects.order_by("-id")
    serializer_class = QuestRunSerializer
    renderer_classes = [JSONRenderer]
    
    def retrieve(self, request, pk=None):
        quest_run = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = QuestRunSerializer(quest_run, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        quest_runs = self.get_queryset().filter(user=request.user)
        serializer = QuestRunSerializer(quest_runs, many=True)
        return Response(serializer.data)


