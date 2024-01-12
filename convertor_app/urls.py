from django.urls import path
from .views import HomePageView,external_api_view,allDailyList,DetailDailyupdate
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
    title='Convertor API',
    default_version = 'v1',
    description = 'API for conversion',
    terms_of_service= "https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@convapi.local"),
    license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[]
    
)

urlpatterns = [
    path('',HomePageView.as_view(), name ='home'),
    path('ext/', external_api_view, name='ext_api'),
    path('alllist/',allDailyList.as_view(),name='full_list'),
    path('detail/<int:pk>/',DetailDailyupdate.as_view(),name='full_list'),
    path('openapi/',schema_view.without_ui(cache_timeout=0)),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name ='schema-swagger-ui'),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0),name ='schema-redoc'),
]