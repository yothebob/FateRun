from django.db import models
    
class QuestRun(models.Model):
    quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="quest_runs")
    completed = models.BooleanField(default=False)
    miles = models.FloatField(default=0.0)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_runs")
