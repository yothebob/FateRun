from django.db import models

# Create your models here.
class Adventure(models.Model):
    public = models.BooleanField(default=False) # share with others
    rating = models.FloatField(default=0.0)
    genre = models.CharField(max_length=255, default="", blank=False, null=False)
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    creator = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_adventures")
    starting_quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="quest_adventure")
    tags = models.ForeignKey("Tag", on_delete=models.SET_NULL, blank=True, null=True, related_name="adventure_tags")
