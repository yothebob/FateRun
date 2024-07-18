from django.db import models
                            
class Song(models.Model):
    url = models.CharField(max_length=255, default="", blank=False, null=False)
    fname = models.CharField(max_length=255, default="", blank=False, null=False)
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    author = models.CharField(max_length=255, default="", blank=False, null=False)
    image = models.CharField(max_length=255, default="", blank=False, null=False)
    tags = models.ForeignKey("Tag", on_delete=models.SET_NULL, blank=True, null=True, related_name="song_tags") # should this me many to many?
