from django.db import models

class Dailyupdate(models.Model):
    date = models.DateTimeField()
    basecurr = models.CharField(max_length=200)
    targetcurr = models.CharField(max_length=200)
    rates = models.IntegerField()

    
