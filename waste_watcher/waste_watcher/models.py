from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    score = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    last_time_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.score})" 
    
class Trashbin(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    amount = models.FloatField(default=0.0)
    max_amount = models.FloatField(default=0.0)