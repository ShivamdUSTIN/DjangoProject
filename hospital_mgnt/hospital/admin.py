from django.contrib import admin
from .models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone', 'email')
    search_fields = ('name', 'specialization')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'phone', 'email')
    search_fields = ('name', 'phone')

# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ('doctor', 'patient', 'date', 'time', 'status')
#     list_filter = ('status', 'date')
#     search_fields = ('doctor__name', 'patient__name')

from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'doctor', 'date')
    search_fields = ('name', 'email', 'phone', 'doctor__name')
    ordering = ('-date', '-time')
    
    # If you want to make the status editable directly from the list view
    list_editable = ('status',)    
