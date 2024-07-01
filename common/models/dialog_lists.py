from django.db import models
                            
class DialogList(models.Model):
    quests = models.ManyToManyField("Quest", related_name="dialogs") # the many to many is only for songs to use
    # quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="dialogs")
    index = models.IntegerField(default=0)
    url = models.CharField(max_length=255, default="", blank=False, null=False)
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    author = models.CharField(max_length=255, default="", blank=False, null=False)
    tags = models.ForeignKey("Tag", on_delete=models.SET_NULL, blank=True, null=True, related_name="dialog_tags")
