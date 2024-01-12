from django.shortcuts import render,get_object_or_404
from rest_framework import generics,permissions
from .models import Dailyupdate
from .serializers import DailyupdateSerializer
import requests,os
from dotenv import load_dotenv
from datetime import datetime
from django.views.generic import TemplateView
from .models import Dailyupdate,User
from .permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
import django_filters.rest_framework as filters
import django_filters

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
        user1= User.objects.get(username= 'old_user')
        datas=Dailyupdate.objects.create(
                    user = user1,
                    date=formatted_date,
                    basecurr=data['base_code'],
                    targetcurr=data['target_code'],
                    rates=data['conversion_rate'],
            )
        
        return render(request,'convertor_app/extapi.html',{'datas':datas})
    else:
        return render(request, 'convertor_app/error.html', {'error_message': 'Failed to fetch data from API'})
    
class ConvertorFilter(django_filters.FilterSet):
    rate=filters.NumberFilter(field_name='rates',lookup_expr='gte')
    basecur_start = filters.CharFilter(field_name='basecurr',lookup_expr='startswith')
    class Meta :
        model = Dailyupdate
        fields = ['id','user','date','basecur_start','targetcurr','rate']


class allDailyList(generics.ListCreateAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ConvertorFilter

    @swagger_auto_schema(operation_description='Retrieve the list of conversions')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Create a new conversion')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        try :
            serializer.save()           
        except ValidationError as e:
            raise ValidationError(detail=e.detail)




class DetailDailyupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dailyupdate.objects.all()
    serializer_class = DailyupdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_description='Retrieve a conversion by id')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Update a single conversion')
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='Delete a conversion')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError(detail=e.detail)
        
    def perform_destroy(self, instance):
        instance.delete()