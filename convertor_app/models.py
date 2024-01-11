from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core import validators


def validate_age(value):
    if value and (value < 18):
        raise ValidationError('Age should be above 18')
    
def valid_email(value):
    if value and value.endswith('.xed'):
        raise ValidationError("Email address should end with '.com' or '.de'")
    
class User(models.Model):
    username = models.CharField(max_length=50,unique=True,null=True,)
    email = models.EmailField(unique=True,null=True,validators=[valid_email,validators.EmailValidator(message='enter a valid email')])
    age = models.PositiveIntegerField(null=True,default='25',validators=[validate_age])
    joining_time = models.DateTimeField(default=datetime.now)

    def clean(self) :
        if not self.joining_time:
            self.joining_time = datetime.now()
            
    def save(self,*args,**kwargs):
        self.full_clean()
        return super().save(*args,**kwargs)
    def __str__(self) :
        return self.username

class Meta:
        ordering = ['username']
        constraints = [models.UniqueConstraint(fields=['username','email'],name='unique email/username')]
        db_table = 'users table'
        verbose_name = 'users for the app'

class Dailyupdate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    basecurr = models.CharField(max_length=20)
    targetcurr = models.CharField(max_length=20)
    rates = models.DecimalField(max_digits=6, decimal_places=4)

    def save(self,*args,**kwargs):#
        self.full_clean()
        return super().save(*args,**kwargs)
    
    def __str__(self) :
        return self.user.username
    
    class Meta :
        ordering =['date']
        verbose_name = 'user conversions'

    
