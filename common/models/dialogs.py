from django.db import models
                            
class Dialog(models.Model):
    quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="dialogs")
    index = models.IntegerField(default=0)
    url = models.CharField(max_length=255, default="", blank=False, null=False)
    tags = models.ForeignKey("Tag", on_delete=models.SET_NULL, blank=True, null=True, related_name="dialog_tags")
