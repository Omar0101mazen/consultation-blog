from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AppointmentForm
from .models import Appointment, AvailableTime, Message
from django.contrib import messages
from .forms import AvailableTimeForm, MessageForm
from main_page.models import Post
from main_page.forms import post_form
from Accounts.models import Profile

@login_required
def manage_available_times(request):
    if request.user.profile.account_type != "advisor":
        return HttpResponseForbidden("You are not authorized to view this page")
    if request.method == 'POST':
        form = AvailableTimeForm(request.POST)
        if form.is_valid():
            available_time = form.save(commit=False)
            available_time.advisor = request.user  # Set the current user as the advisor
            available_time.save()
            return redirect('advisor:advisor_dashboard')
    else:
        form = AvailableTimeForm()

    # Retrieve current user's available times to display
    available_times = AvailableTime.objects.filter(advisor=request.user).order_by('start_time')
    return render(request, 'manage_available_times.html', {'form': form, 'available_times': available_times})


@login_required
def book_appointment(request, advisor_id):
    advisor = get_object_or_404(User, id=advisor_id, profile__account_type='advisor')
    if request.method == 'POST':
        form = AppointmentForm(request.POST, advisor_id=advisor_id)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            # Set the date and time from the available time
            appointment.session_date = form.cleaned_data['available_time'].start_time
            appointment.save()
            # Mark the time slot as booked
            available_time = form.cleaned_data['available_time']
            available_time.is_booked = True
            available_time.save()
            return redirect('dashboard:creat_post')
    else:
        form = AppointmentForm(advisor_id=advisor_id)

    return render(request, 'book_appointment.html', {'form': form, 'advisor': advisor})

    return render(request, 'book_appointment.html', {'appointment_form': appointment_form, 'message_form': message_form, 'advisor': advisor})

def list_advisors(request):
    # Assuming 'profile__account_type' is used to distinguish advisors
    advisors = User.objects.filter(profile__account_type='advisor')
    return render(request, 'list_advisors.html', {'advisors': advisors})



def send_message_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.appointment = appointment
            message.sender = request.user
            message.save()
            return redirect('advisor:advisor_dashboard')  # Or wherever you want to redirect after sending the message
    else:
        form = MessageForm()
    return redirect('advisor:advisor_dashboard')  # Redirect if not a POST request or form is not valid

@login_required
def advisor_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.user.profile.account_type != "advisor":
        return HttpResponseForbidden("You are not authorized to view this page")
    user_posts = Post.objects.filter(author_id=request.user.id)
    user_appointments = Appointment.objects.filter(client=request.user).order_by('-session_date')
    user_photo = Profile.objects.filter(user_id=request.user.id)
    appointments = Appointment.objects.filter(advisor=request.user).order_by('-session_date')
    appointments_with_messages = [{
        'appointment': appointment,
        'messages': Message.objects.filter(appointment=appointment)
    } for appointment in appointments]

    form = post_form()
    message_form = MessageForm()  # Assuming MessageForm is your form class
    return render(request, 'advisor_dashboard.html', {
        'appointments': appointments,
        'form': form,
        'message_form': message_form,
        'user_posts': user_posts,
        'user_appointments': user_appointments,
        'photo': user_photo,
        'appointments_with_messages': appointments_with_messages,
        'profile':profile
    })
    
@login_required
def chat_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.user != appointment.advisor and request.user != appointment.client:
        return HttpResponseForbidden("You are not authorized to view this chat.")

    messages = Message.objects.filter(appointment=appointment).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.appointment = appointment
            new_message.sender = request.user
            new_message.save()
            return redirect('chat_page', appointment_id=appointment_id)
    else:
        form = MessageForm()

    return render(request, 'chat_page.html', {
        'appointment': appointment,
        'messages': messages,
        'form': form
    })
    
@login_required
def user_chat_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, client=request.user)
    messages = Message.objects.filter(appointment=appointment).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.appointment = appointment
            new_message.sender = request.user
            new_message.save()
            return redirect('/', appointment_id=appointment_id)
    else:
        form = MessageForm()

    return render(request, 'user_chat_page.html', {
        'appointment': appointment,
        'messages': messages,
        'form': form
})