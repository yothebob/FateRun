import json
from django.urls import path, include
from common.models import Quest, DialogList
from rest_framework import serializers

# Serializers define the API representation.
class QuestSerializer(serializers.ModelSerializer):

    dialogs = serializers.SerializerMethodField()

    def get_dialogs(self, obj):
        dialog_list = DialogList.object.filter(quest__id=obj.id).first()
        if dialog_list:
            return json.loads(dialog_list.dlist)
        return []
    
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


