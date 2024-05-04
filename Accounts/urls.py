from django.urls import path
from . import views
from .views import *
app_name = 'Accounts'
urlpatterns = [
    
    path('signup/',views.signup, name='signup'),

    path('logout/', views.custom_logout_view, name='custom_logout'),
    path('custom_login_view/',custom_login_view,name= 'custom_login_view')
    
    
]