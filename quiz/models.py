from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Quiz(models.Model):
    private = models.BooleanField()
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    participants = models.IntegerField()
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    rounds = models.IntegerField()
    numqs = models.IntegerField(default=0)

    def summary(self):
        return self.body[:200]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def __str__(self):
        return self.title


class Round(models.Model):
    title = models.CharField(max_length=200)
    # number = models.IntegerField(default=1)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Questions(models.Model):
    prompt = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def __str__(self):
        return self.prompt
