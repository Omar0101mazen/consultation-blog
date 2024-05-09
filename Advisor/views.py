from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.http import HttpResponseForbidden, HttpResponseRedirect
from ..Accounts import User, Appointment
from .forms import AppointmentForm

# Create your views here.
@login_required
def advisor(request):
    if not request.user.profile.is_advisor:
        return HttpResponseForbidden("You are not authorized to view this page")
    appointments = Appointment.objects.filter(advisor=request.user).order_by('date')
    return render(request, 'Advisor/advisor_dashboard.html', {'appointments': appointments})

@login_required
def book_appointment(request, advisor_id):
    if request.user.profile.is_advisor:
        return HttpResponseForbidden("Advisors cannot book appointments.")
    advisor = User.objects.get(pk=advisor_id, profile__is_advisor=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.advisor = advisor
            appointment.save()
            return redirect('profile')
    else:
        form = AppointmentForm()
    return render(request, 'Advisor/book_appointment.html', {'form': form})
