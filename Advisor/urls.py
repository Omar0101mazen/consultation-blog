from django.urls import path
from . import views
from .views import *
app_name = 'Advisor'
urlpatterns = [
    
    path('user/',views.advisor,name='user')
       
]