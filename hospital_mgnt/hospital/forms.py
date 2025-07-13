from django import forms
from .models import GetInTouch
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone']

from django import forms
from .models import GetInTouch

class GetInTouchForm(forms.ModelForm):
    class Meta:
        model = GetInTouch
        fields = ['name', 'phone_number', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message',
                'class': 'message-box',
                'rows': 3  # You can add other textarea attributes here
            }),
        }