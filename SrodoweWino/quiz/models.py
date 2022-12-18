from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.question}: {self.answer}'

class Players(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    # A field to track the current player
    current_player = models.BooleanField(default=False)