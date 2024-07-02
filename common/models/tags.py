from django.db import models
# Create your models here.

class Tag(models.Model):

    def __str__(self):
        return f"{self.prompt} - Folder:{self.name}"

    
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    prompt = models.CharField(max_length=255, default="", blank=False, null=False)
