from django.shortcuts import render,get_object_or_404
from rest_framework import generics,permissions
from .models import Dailyupdate
from .serializers import DailyupdateSerializer
import requests,os,json
from dotenv import load_dotenv
from django.http import HttpResponse
from datetime import datetime

# Create your views here.


class DetailDailyupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer

def home(request):
    return HttpResponse('<h1>Welcome to Daily updates</h1>')


def external_api_view(request):
    api_url = 'https://v6.exchangerate-api.com/v6/pair/EUR/INR'
    load_dotenv()
    api_key= os.environ.get('ak')
    #print (api_key)
    headers = {'Authorization': f'{api_key}'} 

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #print (data)
        date_str = data['time_last_update_utc']
        formatted_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')

        datas=Dailyupdate.objects.create(
                    date=formatted_date,
                    basecurr=data['base_code'],
                    targetcurr=data['target_code'],
                    rates=data['conversion_rate'],
            )
        
        return render(request,'convertor_app/extapi.html',{'datas':datas})
    else:
        return render(request, 'convertor_app/error.html', {'error_message': 'Failed to fetch data from API'})
    
class allDailyList(generics.ListCreateAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer