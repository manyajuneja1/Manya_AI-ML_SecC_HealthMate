from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Auth routes
    path('register/', views.select_registration, name='register'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.custom_login, name='login'),
   # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Patient dashboard route
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('', views.frontend, name='frontend'),
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('appointment/update/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('notifications/dismiss/<int:notification_id>/', views.dismiss_notification, name='dismiss_notification'),
    path('send_message/', views.send_message, name='send_message'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)