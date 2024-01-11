from django.urls import path
from .views import HomePageView,external_api_view,allDailyList,DetailDailyupdate

urlpatterns = [
    path('',HomePageView.as_view(), name ='home'),
    path('ext/', external_api_view, name='ext_api'),
    path('alllist/',allDailyList.as_view(),name='full_list'),
    path('detail/<int:pk>/',DetailDailyupdate.as_view(),name='full_list'),
]