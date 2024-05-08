from django.urls import path
from . import views
from .views import *
app_name = 'dash_board'
urlpatterns = [
    
    path('creat_post/',views.creat_post, name='creat_post'),


    
]