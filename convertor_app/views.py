from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Dailyupdate
from .serializers import DailyupdateSerializer
import requests,os

# Create your views here.
class allDailyList(generics.ListCreateAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer

class DetailDailyupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer




def external_api_view(request):
    api_url = 'https://v6.exchangerate-api.com/v6/pair/EUR/INR'
    api_key= os.getenv('ak')
    headers = {'X-API-KEY': f'{api_key}'} 

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #print (data)
        for item in data:
            Dailyupdate.objects.create(
                    date=item['time_last_update_utc'],
                    basecurr=item['base_code'],
                    targetcurr=item['target_code'],
                    rates=item['conversion_rate'],
            )
    else:
        return render(request, 'myapp/error.html', {'error_message': 'Failed to fetch data from API'})