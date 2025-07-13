from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('Home', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('departments/', views.departments_view, name='departments'),
    
    # Appointment URLs (only one endpoint needed)
    path("make-appointment/", views.make_appointment, name="make_appointment"),
    path('get-available-doctors/', views.get_available_doctors, name='get_available_doctors'),
    
    # Remove this duplicate line:
    # path('book-appointment/', views.book_appointment, name='book_appointment'),
    
    # Other admin URLs
    path('view_doctor/', views.view_Doctor, name='view_doctor'),
    path('Delete_Doctor/<int:pid>/', views.Delete_Doctor, name='Delete_Doctor'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('view_Patient/', views.view_patient, name='view_patient'),
    path('Delete_Patient/<int:pid>/', views.Delete_Patient, name='Delete_Patient'),
    path('AddDoctor/', views.AddDoctor, name='AddDoctor'),
    path('test-db/', views.test_db, name='test_db'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('our-doctors/', views.doctors_public_view, name='our_doctors'),
]