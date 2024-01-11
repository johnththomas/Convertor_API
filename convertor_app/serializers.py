from rest_framework import serializers
from .models import Dailyupdate
from datetime import datetime
from rest_framework.exceptions import ValidationError


class PastDateValidator:
    def __call__(self, value) :
        if value > datetime.now():
            raise ValidationError("Published date must be in the past.")



class DailyupdateSerializer(serializers.ModelSerializer):
    Date = serializers.DateTimeField(required=True, validators=[PastDateValidator()])
    class Meta:
        model = Dailyupdate
        #fields = '__all__'
        fields = ['id','Date','basecurr','targetcurr','rates']