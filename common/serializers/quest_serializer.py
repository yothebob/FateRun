import json
from django.urls import path, include
from common.models import Quest
from rest_framework import serializers

# Serializers define the API representation.
class QuestSerializer(serializers.ModelSerializer):

    dialogs = serializers.SerializerMethodField()

    def get_dialogs(self, obj):
        return json.loads(obj.dialog_list.dlist)
    
    class Meta:
        model = Quest
        fields = [
            "id",
            "uuid",
            "name",
            "dialogs",
            "creator",
            "rating",
            "public"
        ]

class QuestListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quest
        fields = [
            "id",
            "name",
            "rating",
            "public"
        ]


