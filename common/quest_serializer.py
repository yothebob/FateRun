from django.urls import path, include
from common.models import Quest
from rest_framework import serializers

# Serializers define the API representation.
class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = [
            "prompt",
            "generated_response",
            "uuid",
            "creator"
        ]


