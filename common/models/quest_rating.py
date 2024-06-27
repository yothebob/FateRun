from django.db import models

class QuestRating(models.Model):
    quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="rated_quest")
    rating = models.FloatField(default=0.0)
