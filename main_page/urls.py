from django.urls import path
from . import views
from .views import *
app_name = 'main_page'
urlpatterns = [


    path('',views.post_list, name='list'),
    path('<int:slug>',views.post_detail, name='detail'),

]