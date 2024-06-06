from django.db import models

# Create your models here.
class Quest(models.Model):
    prompt = models.TextField(blank=True, null=True) 
    generated_response = models.TextField(blank=True, null=True) # this will allways need to be processed into a list split \n
    # public = models.BooleanField(default=False) # share with others
    # rating = models.FloatField(default=0.0)
    uuid = models.CharField(max_length=125, default="", blank=False, null=False)
    creator = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_quests")

    
class QuestRun(models.Model):
    quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="quest_runs")
    completed = models.BooleanField(default=False)
    miles = models.FloatField(default=0.0)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_runs")
