from rest_framework import serializers
from .models import Dailyupdate

class DailyupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dailyupdate
        fields = '__all__'