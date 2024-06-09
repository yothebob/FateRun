from django.urls import path, include
from common.models import Quest
from rest_framework import serializers

# Serializers define the API representation.
class QuestSerializer(serializers.ModelSerializer):

    dialogs = serializers.SerializerMethodField()

    def get_dialogs(self, obj):
        res = []
        for i in obj.dialogs.order_by("index"):
            if i:
                res.append(i.url)
        return res

    class Meta:
        model = Quest
        fields = [
            "id",
            "uuid",
            "dialogs",
            "creator"
        ]


