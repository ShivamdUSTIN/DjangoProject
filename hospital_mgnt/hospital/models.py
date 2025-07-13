from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(default='no-email@example.com')
    phone = models.CharField(max_length=15)
    #doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.date} at {self.time}"
    
    def send_confirmation_email(self):
        subject = f"Appointment Confirmation with Dr. {self.doctor.name}"
        message = f"""
        Dear {self.name},
        
        Your appointment has been confirmed with Dr. {self.doctor.name} ({self.doctor.specialization}).
        
        Appointment Details:
        Date: {self.date}
        Time: {self.time}
        
        Doctor Contact:
        Phone: {self.doctor.phone}
        Email: {self.doctor.email}
        
        Please arrive 15 minutes before your scheduled time.
        
        Thank you,
        {settings.SITE_NAME}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

    # Add this method to display patient name in admin
    def patient_name(self):
        return self.name
    patient_name.short_description = 'Patient'



    from django.db import models

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    generic_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.batch_number}) - Exp: {self.expiry_date}"
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'

# hospital/models.py

from django.db import models

class GetInTouch(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
