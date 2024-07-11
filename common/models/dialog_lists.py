from django.db import models
                            
class DialogList(models.Model):
    quest = models.ForeignKey("Quest", on_delete=models.SET_NULL, blank=True, null=True, related_name="dialog_list")
    dlist = models.TextField(default="[]")
