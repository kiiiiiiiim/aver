from django.db import models
from django.utils import timezone


# Create your models here.


class Club(models.Model):
    name = models.CharField(max_length=20)


class Location(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=512)


class Score(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True)

    def add_score(self, name, date, score, location, club):
        self.score = score
        self.date = date
        self.name = name
        self.location = location
        self.club = club
        self.save()
