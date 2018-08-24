from django.db import models
from django.utils import timezone


# Create your models here.


class Score(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()

    def add_score(self, name, date, score):
        self.score = score;
        self.date = date;
        self.name = name;
        self.save()
