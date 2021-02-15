from django.db import models
from django.utils import timezone

import datetime

# Create your models here.

class Questions(models.Model):
    questions_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('some date')

    def __str__(self):
        return self.questions_text

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

class Choise(models.Model):
    question = models.ForeignKey(Questions, on_delete= models.CASCADE)
    choise_text = models.CharField(max_length = 100)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choise_text

