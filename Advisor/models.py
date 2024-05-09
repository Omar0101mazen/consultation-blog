from django.db import models
from django.conf import settings


# Create your models here.
from django.db import models
from django.conf import settings

class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="client_appointments", on_delete=models.CASCADE)
    advisor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="advisor_appointments", on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date} - {self.client.username} with {self.advisor.username}"
