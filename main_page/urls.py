from django.urls import path
from . import views
from .views import *
app_name = 'main_page'
urlpatterns = [


    path('',views.post_list, name='list'),
    path('<int:slug>',views.post_detail, name='detail'),
    path('about/',views.about,name='about'),
    path('rate_comment/<int:comment_id>/', rate_comment, name='rate_comment'),

]
