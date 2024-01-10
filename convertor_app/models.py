from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core import validators


def validate_age(value):
    if value and (value < 18):
        raise ValidationError('Age should be above 18')
    
def valid_email(value):
    if value and value.notendswith('.com','.de'):
        raise ValidationError("Email address should end with '.com' or '.de'")
    
class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True,validators=[valid_email,validators.EmailValidator(message='enter a valid email')])
    age = models.PositiveIntegerField(null=True,validators=[validate_age])
    joining_time = models.DateTimeField(default=timezone.now)

    def clean(self) :
        if not self.joining_time:
            self.joining_time = timezone.now()
            
    def save(self,*args,**kwargs):
        self.full_clean()
        return super().save(*args,**kwargs)
    def __str__(self) :
        return self.username


class Dailyupdate(models.Model):
    date = models.DateTimeField()
    basecurr = models.CharField(max_length=20)
    targetcurr = models.CharField(max_length=20)
    rates = models.DecimalField(max_digits=6, decimal_places=3)

    
