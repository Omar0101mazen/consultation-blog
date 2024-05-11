from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment, AvailableTime, Message

class AppointmentForm(forms.ModelForm):
    session_reason = forms.CharField(label='سبب الجلسة', max_length=255)
    session_type = forms.ChoiceField(label='نوع الجلسة', choices=Appointment.SESSION_TYPES)
    available_time = forms.ModelChoiceField(
        queryset=AvailableTime.objects.none(),
        label='Available Times',
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['session_reason', 'session_type']  # Remove 'available_time' from here

    def __init__(self, *args, **kwargs):
        advisor_id = kwargs.pop('advisor_id', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.initial['advisor_id'] = advisor_id  # Store advisor ID in initial for use during save
        if advisor_id:
            self.fields['available_time'].queryset = AvailableTime.objects.filter(
                advisor_id=advisor_id, 
                is_booked=False
            ).order_by('start_time')

    def save(self, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)
        # Set the advisor here if not already set
        if not instance.advisor_id:
            instance.advisor_id = self.initial['advisor_id']
            
        # Set date and time from the chosen available time
        available_time = self.cleaned_data['available_time']
        instance.session_date = available_time.start_time.date()
        instance.session_time = available_time.start_time.time()
        if commit:
            instance.save()
            # Mark the time slot as booked after saving the appointment
            available_time.is_booked = True
            available_time.save()
        return instance


    
class AvailableTimeForm(forms.ModelForm):
    class Meta:
        model = AvailableTime
        fields = ['start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']