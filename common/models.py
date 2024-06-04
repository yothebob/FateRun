from django.db import models

# Create your models here.
class Run(models.Model):
    prompt = models.TextField(blank=True, null=True)
    generated_response = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    miles = models.FloatField(default=0.0)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True, related_name="user_runs")
