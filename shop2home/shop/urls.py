# myapp/urls.py
from django.urls import path
from .views import upload_csv,search,home

 

urlpatterns = [
    path('', home , name ='home'),
    path('upload_csv/', upload_csv , name='upload_csv'),
    path('search/', search, name='search'),
    
]
