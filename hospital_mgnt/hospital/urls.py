from django.urls import path,include
from . import views
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('', views.Index, name='index'),
    path('Home', views.Home, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    
    # Admin dashboard URL
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    
    
    # Authentication URLs
    path('accounts/', include(tf_urls)),
    
    # Your other URLs remain the same
    path('logout/', views.Logout_admin, name='logout_admin'),
    path('doctor/', views.doctor, name='doctor'),
    path('index/', views.Index, name='index'),
    path('departments/', views.Departments, name='departments'),
    

    path("make-appointment/", views.make_appointment, name="make_appointment"),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('view_doctor/', views.view_Doctor, name='view_doctor'),
    path('Delete_Doctor/<int:pid>/', views.Delete_Doctor, name='Delete_Doctor'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('view_Patient/', views.view_patient, name='view_patient'),
    path('Delete_Patient/<int:pid>/', views.Delete_Patient, name='Delete_Patient'),
    path('AddDoctor/', views.AddDoctor, name='AddDoctor'),
    path('test-db/', views.test_db, name='test_db'),
    path('get-available-doctors/', views.get_available_doctors, name='get_available_doctors'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
]