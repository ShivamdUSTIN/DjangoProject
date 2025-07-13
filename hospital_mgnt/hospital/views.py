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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from auth_app.middlewares import auth, guest



def logout_view(request):
    logout(request)
    return redirect('login')





def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

@auth
def view_Doctor(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)


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

def Departments(request):
    return render(request,'departments.html')

def Index(request):
    return render (request , 'index.html')

@auth
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


# Admin-protected views

def view_Doctor(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)

def view_patient(request):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doc = Patient.objects.all()
    d = {'doc': doc}
    return render(request, 'view_patient.html', d)


def Delete_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')


def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('two_factor:login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')


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


def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@version")
            row = cursor.fetchone()
        return HttpResponse(f"Database connection successful! SQL Server version: {row[0]}")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {str(e)}")
    

# @csrf_exempt  # Optional: Only use this if you're testing without CSRF token
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


def departments_view(request):
    departments = [
        {
            "name": "Cardiology",
            "image": "images/s1.png",
            "description": "Experienced surgeons in beating heart & bloodless surgeries."
        },
        {
            "name": "Diagnosis",
            "image": "images/s2.png",
            "description": "Advanced diagnostic services with rapid results."
        },
        {
            "name": "Anaesthesiology",
            "image": "images/s3.png",
            "description": "Pain management and patient care before, during and after surgery."
       },
        {
            "name": "First Aid",
            "image": "images/s4.png",
            "description": "Emergency care for quick stabilization and triage."
        },
        {
            "name": "Neurology",
            "image": "images/s5.png",
            "description": "Comprehensive care for brain and nervous system disorders."
        },
        {
            "name": "Orthopaedics",
            "image": "images/s6.png",
            "description": "Treatment of bones, joints, ligaments, and muscles."
        },
    ]
    return render(request, 'departments.html', {'departments': departments})






from django.shortcuts import render, redirect
from django.contrib import messages  # Add this import
from .forms import GetInTouchForm

def contact_view(request):
    if request.method == 'POST':
        form = GetInTouchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for getting in touch!')
            return redirect('contact')  # Redirect to clear POST data
    else:
        form = GetInTouchForm()
    return render(request, 'contact.html', {'form': form})

def doctors_public_view(request):
    doctors = Doctor.objects.all().order_by('-id')[:8]  # Latest 8 doctors
    return render(request, 'doctors.html', {'doctors': doctors})

def make_appointment(request):
    if request.method == "POST":
        try:
            # Handle both form-data and JSON requests
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
            
            doctor = Doctor.objects.get(id=data.get('doctor'))
            
            appointment = Appointment(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                doctor=doctor,
                date=data.get('date'),
                time=data.get('time'),
                message=data.get('message', '')
            )
            appointment.save()
            
            return JsonResponse({
                "success": True,
                "message": "Appointment booked successfully!"
            })
        except Doctor.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Selected doctor does not exist"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "success": False,
        "message": "Invalid request method"
    }, status=405)
