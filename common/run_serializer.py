from django.urls import path, include
from common.models import Run
from rest_framework import serializers

# Serializers define the API representation.
class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = [
            "prompt",
            "generated_response",
            "completed",
            "miles",
            "start_time",
            "end_time",
            "user"
        ]


