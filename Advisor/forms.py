from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date']

    def clean_date(self):
        date = self.cleaned_data['date']
        if Appointment.objects.filter(date=date).exists():
            raise ValidationError(_('This date is already booked for an appointment.'))
        return date
