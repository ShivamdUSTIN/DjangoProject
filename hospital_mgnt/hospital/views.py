from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import AppointmentForm
from .models import Doctor, Patient, Appointment
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import connection
import json
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django_otp.models import Device


# Use these imports instead
from django_otp.decorators import otp_required
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required

@login_required
@otp_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@otp_required
def view_Doctor(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)

@login_required
@otp_required
def AddDoctor(request):
    error = ""
    if request.method == "POST":
        # Your existing AddDoctor code
        pass
    return render(request, 'add_doctor.html', {'error': error})

# Regular views (no auth required)
def About(request):
    return render(request, 'about.html')

def Home(request):
    return render(request, 'home.html')

def Contact(request):
    return render(request, 'contact.html')

def Departments(request):
    return render(request,'departments.html')

def doctor(request):
    return render(request, 'doctors.html')

# Authentication views
# def Index(request):
#     if not request.user.is_staff:
#         return redirect('two_factor:login')
#     return render(request, 'index.html')

def Index(request):
    return render (request , 'index.html')

# @login_required
# def admin_dashboard(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         if not request.user.otp_device:
#             return redirect(reverse('two_factor:setup'))
#         return render(request, 'admin_dashboard.html')
#     return redirect('home')

# @login_required
# @otp_required
# def admin_dashboard(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         if not request.user.otp_device:
#             return redirect(reverse('two_factor:setup'))
#         return render(request, 'admin_dashboard.html')
#     return redirect('home')

from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required

@login_required
@otp_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

# @login_required
# @otp_required
# def admin_dashboard(request):
#     if request.user.is_staff:
#         return render(request, 'admin_dashboard.html')
#     return redirect('index')


def Logout_admin(request):
    if request.user.is_authenticated:
        Device.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('home')

# Admin-protected views
@otp_required
def view_Doctor(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)

@otp_required
def view_patient(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Patient.objects.all()
    d = {'doc': doc}
    return render(request, 'view_patient.html', d)

@otp_required
def Delete_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

@otp_required
def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

@otp_required
def AddDoctor(request):
    error = ""
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')
        email = request.POST.get('email')

        if not name or not phone or not specialization or not email:
            error = "All fields are required."
        else:
            try:
                if Doctor.objects.filter(phone=phone).exists():
                    error = "Phone number already exists."
                elif Doctor.objects.filter(email=email).exists():
                    error = "Email already exists."
                else:
                    Doctor.objects.create(
                        name=name,
                        phone=phone,
                        specialization=specialization,
                        email=email
                    )
                    return redirect('view_doctor')
            except IntegrityError:
                error = "Database error, please try again later."
            except Exception as e:
                error = f"An unexpected error occurred: {str(e)}"
    return render(request, 'add_doctor.html', {'error': error})

@otp_required
def add_patient(request):
    error = ""
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        address = request.POST.get("address")

        if not name or not phone or not age or not gender or not email or not address:
            error = "All fields are required."
        else:
            try:
                Patient.objects.create(
                    name=name,
                    phone=phone,
                    age=int(age),
                    gender=gender,
                    email=email,
                    address=address
                )
                return redirect('view_patient')
            except IntegrityError:
                error = "Database error, please try again later."
            except Exception as e:
                error = f"An unexpected error occurred: {str(e)}"
    return render(request, "add_Patient.html", {'error': error})

# Appointment views (no auth required)
def appointment_view(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'appointment.html', context)

def make_appointment(request):
    if request.method == "POST":
        try:
            data = request.POST
            doctor = Doctor.objects.get(id=data.get('doctor'))
            
            appointment = Appointment(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                doctor=doctor,
                date=data.get('date'),
                time=data.get('time'),
                message=data.get('message')
            )
            appointment.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "errors": str(e)})
    return JsonResponse({"success": False, "errors": "Invalid request method"})

def get_available_doctors(request):
    try:
        doctors = Doctor.objects.all()
        doctors_data = [{
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.specialization,
            'phone': doctor.phone,
            'email': doctor.email
        } for doctor in doctors]
        return JsonResponse({'success': True, 'doctors': doctors_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def book_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment = Appointment.objects.create(
                patient_name=data['name'],
                patient_email=data['email'],
                patient_phone=data['phone'],
                doctor_id=data['doctor'],
                date=data['date'],
                time=data['time'],
                message=data.get('message', '')
            )
            return JsonResponse({
                'success': True,
                'message': 'Appointment booked successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)

def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@version")
            row = cursor.fetchone()
        return HttpResponse(f"Database connection successful! SQL Server version: {row[0]}")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {str(e)}")
    
    # Add this to views.py

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt  # Optional: Only use this if you're testing without CSRF token
def submit_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if name and email:
            # Do something with the form data (e.g., save to DB)
            return JsonResponse({"success": True, "message": "Form submitted successfully!"})
        else:
            return JsonResponse({"success": False, "message": "Missing fields."})

    return JsonResponse({"success": False, "message": "Invalid request method."})


# In your views.py
    # return render(request, 'two_factor/_base.html', context)
