from django.urls import path, include
from common.models import QuestRun
from rest_framework import serializers

# Serializers define the API representation.
class QuestRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestRun
        fields = [
            "id",
            "quest",
            "completed",
            "miles",
            "start_time",
            "end_time",
            "user",
            "rating"
        ]
