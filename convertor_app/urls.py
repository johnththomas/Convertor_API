from django.urls import path
from .views import home,external_api_view

urlpatterns = [
    path('',home, name ='home'),
    path('ext/', external_api_view, name='ext_api'),
]