from django.urls import path
from . import views
from .views import *
app_name = 'Advisor'
urlpatterns = [
    path('dashboard/', advisor_dashboard, name='advisor_dashboard'),
    path('manage-times/', manage_available_times, name='manage_available_times'),
    path('book-appointment/<int:advisor_id>/', book_appointment, name='book_appointment'),
    path('list-advisors/', list_advisors, name='list_advisors'),
    path('send-message/<int:appointment_id>/', send_message_view, name='send_message'),
    path('chat/<int:appointment_id>/', chat_page, name='chat_page'),
    path('chat_user/<int:appointment_id>/', user_chat_page, name='user_chat_page'),
]