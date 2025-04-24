from re import L
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


# My Imports 
from django.contrib.auth.decorators import login_required
from .models import Patient
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user.profile.role == 'patient':
                    return redirect('patient_dashboard')
            else:
                messages.error(request, "User role not defined.")
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# Function to Render the FrontEnd Page
def frontend(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('backend'))
    else:
        return render(request, "frontend.html")


# BACKEND SECTION 
# Function to Render the BackEnd Page
@cache_control(no_cache = True, must_validate = True, no_store = True)
@login_required(login_url='login')
def backend(request):
    # if its a GET request 
    if 'q' in request.GET:
        q = request.GET['q']
        all_patient_list = Patient.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(age__icontains=q) |  Q(gender__icontains=q) |   Q(note__icontains=q) 
        ).order_by('-created_at')
    else:
        all_patient_list = Patient.objects.all().order_by('-created_at')
    paginator = Paginator(all_patient_list, 10)
    page = request.GET.get('page')
    all_patient = paginator.get_page(page)

    return render(request, 'backend.html', {"patients": all_patient})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            note = request.POST.get('note', '')

            if not all([name, phone, email, age, gender]):
                messages.error(request, "All fields are required.")
                return render(request, 'add.html')

            patient = Patient(
                name=name,
                phone=phone,
                email=email,
                age=age,
                gender=gender,
                note=note
            )
            patient.save()
            messages.success(request, "Patient Added Successfully!")
            return redirect('backend')

        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")
            return render(request, 'add.html')

    # ✅ This line was missing earlier — for GET request
    return render(request, 'add.html')


# Function to Add the Pateint 
@cache_control(no_cache = True, must_validate = True, no_store = True)

        

def new_func(request):
    return render(request, 'add.html')


# Function to Render the Patient's Individual Page 
@cache_control(no_cache = True, must_validate = True, no_store = True)
@login_required(login_url='login')
def patient(request, patient_id):
    patient = Patient.objects.get(id = patient_id)
    if patient != None:
        return render(request, 'edit.html', {'patient': patient})
    

# Function to Edit the Patient's Info
@cache_control(no_cache = True, must_validate = True, no_store = True)
@login_required(login_url='login')
def edit_patient(request):
    # if its a POST request 
    if request.method == 'POST':
        patient = Patient.objects.get( pk = request.POST.get('id') )
        # patient = Patient.objects.get( pk = patient_id )
        if patient != None:
            patient.name = request.POST.get('name')
            patient.phone = request.POST.get('phone')
            patient.email = request.POST.get('email')
            patient.age = request.POST.get('age')
            patient.gender = request.POST.get('gender')
            patient.note = request.POST.get('note')
            patient.save()
            messages.success(request, 'Patient updated successfully')
            return HttpResponseRedirect(reverse('backend'))


# Function to Delete the patient 
@cache_control(no_cache = True, must_validate = True, no_store = True)
@login_required(login_url='login')
def delete_patient(request, patient_id):
    patient = Patient.objects.get( pk = patient_id )
    patient.delete()

    messages.success(request, 'Patient removed successfully')
    return HttpResponseRedirect(reverse('backend'))
from django.shortcuts import render
@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)

    # count summaries for charts
    completed = appointments.filter(status='Completed').count()
    pending = appointments.filter(status='Pending').count()
    cancelled = appointments.filter(status='Cancelled').count()

    return render(request, 'patient_dashboard.html', {
        'appointments': appointments,
        'completed': completed,
        'pending': pending,
        'cancelled': cancelled,
    })
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PatientRegistrationForm
from django.contrib import messages



def login_patient(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('patient_dashboard')  # we'll make this next
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment
from .models import Notification
@login_required
def patient_dashboard(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'patient_dashboard.html', {
        'notifications': notifications,
    })
from collections import Counter
from django.db.models import Count

from .decorators import role_required

@login_required
@role_required('doctor')
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-date')
    completed_count = appointments.filter(status='Completed').count()
    pending_count = appointments.filter(status='Pending').count()
    cancelled_count = appointments.filter(status='Cancelled').count()
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'notifications': notifications,
    })

@login_required  
@role_required('patient')  
def patient_dashboard(request):
    appointments = Appointment.objects.all()
    return render(request, 'patient_dashboard.html', {'appointments': appointments})
def frontend(request):
    return render(request, 'frontend.html')
def symptom_checker(request):
    return render(request, 'symptom_checker.html')
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Appointment

@require_POST
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('status')
    if new_status in ['Pending', 'Completed', 'Cancelled']:
        appointment.status = new_status
        appointment.save()
    return redirect('doctor_dashboard')

from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification 


def book_appointment(request):
    doctors = User.objects.filter(profile__role='doctor')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        form.fields['doctor'].queryset = doctors
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'Pending'
            appointment.save()
         #  Email to Doctor
            send_mail(
                subject='🩺 New Appointment Booked on HealthMate',
                message=f"""
Dear Dr. {appointment.doctor.username},

You have a new appointment booked on HealthMate.

🧑‍⚕️ Patient: {appointment.patient.username}
📅 Date: {appointment.date}
⏰ Time: {appointment.time}
📝 Reason: {appointment.reason}

Please check your dashboard for more details.

- HealthMate Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[appointment.doctor.email],
                fail_silently=False,
            )

            # Email to Patient
            send_mail(
                subject='✅ Appointment Confirmation from HealthMate',
                message=f"""
Hi {appointment.patient.username},

Your appointment with Dr. {appointment.doctor.username} has been successfully booked on HealthMate.

📅 Date: {appointment.date}
⏰ Time: {appointment.time}
🩺 Doctor: Dr. {appointment.doctor.username}

Thank you for choosing HealthMate 💖

Stay healthy,
HealthMate Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[appointment.patient.email],
                fail_silently=False,
            )

            # Create notifications
            Notification.objects.create(
             user=appointment.doctor,
            message=f"New appointment booked by {appointment.patient.username}"
            )

            Notification.objects.create(
            user=appointment.patient,
            message=f"Your appointment with Dr. {appointment.doctor.username} is confirmed."
            )
            

            # Optional: add a success message
            messages.success(request, 'Appointment booked successfully! A confirmation email has been sent.')
            return redirect('patient_dashboard')  # or wherever you want to redirect after booking
    else:
        form = AppointmentForm()
        form.fields['doctor'].queryset = doctors
    return render(request, 'book_appointment.html', {
        'form': form,
        'doctors': doctors})
    
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientRegistrationForm


# views.py

from .forms import MessageForm
from django.contrib.auth.decorators import login_required

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('doctor_dashboard')  # or a messages page
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})
from .models import Notification

def send_notification(user, message):
    Notification.objects.create(user=user, message=message)
    from django.core.mail import send_mail

def send_notification(to_email, subject, message):
    send_mail(
        subject,
        message,
        'your_email@gmail.com',
        [to_email],
        fail_silently=False,
    )
from django.shortcuts import get_object_or_404, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required
def dismiss_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})
def select_registration(request):
    return render(request, 'registration/register.html')
from django.contrib.auth import login
from .forms import DoctorRegistrationForm
from .models import Profile

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = 'doctor'
            user.profile.save()
            login(request, user)
            messages.success(request, f"Welcome Dr. {user.username}!")
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'registration/register_doctor.html', {'form': form})
from .forms import PatientRegistrationForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid ✅") 
            user = form.save()
            user.profile.role = 'patient'
            user.profile.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}, account created!")
            return redirect('patient_dashboard')
        else:
            print("Form is invalid:", form.errors)  # See what’s wrong
            messages.error(request, 'Please correct the errors below.')
            messages.error(request, "Something went wrong. Check your inputs.")
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'registration/register_patient.html', {'form': form})
from django.contrib import messages

@require_POST
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('status')

    if new_status in ['Pending', 'Completed', 'Cancelled']:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Appointment marked as {new_status}.")

    return redirect('doctor_dashboard')
