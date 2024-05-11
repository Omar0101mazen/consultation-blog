from django.contrib import admin
from .models import Appointment, AvailableTime, Message
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AvailableTime)
admin.site.register(Message)