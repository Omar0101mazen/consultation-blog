from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Appointment(models.Model):
    SESSION_TYPES = (
        ('video', _('فيديو')),
        ('audio', _('صوت')),
        ('text', _('رسائل')),
    )

    client = models.ForeignKey(
        User, 
        related_name='client_appointments', 
        on_delete=models.CASCADE,
        limit_choices_to={'profile__account_type': 'normal'},  # Ensures the client is a normal user
        verbose_name=_("Client")
    )
    advisor = models.ForeignKey(
        User, 
        related_name='advisor_appointments', 
        on_delete=models.CASCADE,
        limit_choices_to={'profile__account_type': 'advisor'},  # Ensures the advisor is an advisor
        verbose_name=_("Advisor")
    )
    session_reason = models.CharField(max_length=255, verbose_name=_("سبب الجلسة"), null=True)
    session_type = models.CharField(max_length=50, choices=SESSION_TYPES, verbose_name=_("نوع الجلسة"), null=True)
    session_date = models.DateField(verbose_name=_("تاريخ الجلسة"), default=timezone.now)
    session_time = models.TimeField(verbose_name=_("وقت الجلسة"), null=True)

    def str(self):
        return f"{self.session_type} session on {self.session_date} at {self.session_time} with {self.advisor.username}"
    

class AvailableTime(models.Model):
    advisor = models.ForeignKey(User, related_name='available_times', on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    is_booked = models.BooleanField(default=False, verbose_name=_("Is Booked"))

    def str(self):
        return f"{self.advisor.username} available from {self.start_time} to {self.end_time}"
 
class Message(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Message from {self.sender.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"