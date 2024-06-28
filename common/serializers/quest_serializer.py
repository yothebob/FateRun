from django.urls import path, include
from common.models import Quest, QuestRun
from rest_framework import serializers

# Serializers define the API representation.
class QuestSerializer(serializers.ModelSerializer):

    dialogs = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        quest_runs = QuestRun.objects.filter(quest__id=obj.id, rating__gte=1.0).values_list("rating", flat=True)
        return round(sum(quest_runs)/ len(quest_runs), 1)


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
            "name",
            "dialogs",
            "creator",
            "rating",
            "public"
        ]


