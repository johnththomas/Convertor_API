from django.shortcuts import render,get_object_or_404
from rest_framework import generics,permissions
from .models import Dailyupdate
from .serializers import DailyupdateSerializer
import requests,os
from dotenv import load_dotenv
from datetime import datetime
from django.views.generic import TemplateView
from .models import Dailyupdate,User
#from .permissions import IsAdminOrReadOnly
#from rest_framework.authentication import TokenAuthentication



class HomePageView(TemplateView):
    template_name = 'convertor_app/homepage.html'


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
        user= User.objects.create()
        datas=Dailyupdate.objects.create(
                    user = user,
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
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    





class DetailDailyupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    