from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    score = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.score})" 