from rest_framework import serializers
from .models import Dailyupdate
from datetime import datetime
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.utils.html import escape,strip_tags
from django.utils.text import slugify

class PastDateValidator:
    def __call__(self, value) :
        if value > timezone.now():
            raise ValidationError("Published date must be in the past.")

class CapitalizeName:
    def __call__(self, value) :
        return value.title()

class DailyupdateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True, validators=[PastDateValidator()])
    

    def validate_basecurr(self,value):
        return slugify(strip_tags(value))
    
    def to_representation(self, instance):
        instance.basecurr = CapitalizeName()(instance.basecurr) #cap(instance.basecurr)
        instance.targetcurr=CapitalizeName()(instance.targetcurr)
        return super().to_representation(instance)
        
    class Meta:
        model = Dailyupdate
        #fields = '__all__'
        fields = ['id','user','date','basecurr','targetcurr','rates']