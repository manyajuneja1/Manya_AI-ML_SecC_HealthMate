from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from App import views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Include all app-level URLs
    path('', include('App.urls')),

    # Website Frontend Page
    path('home/', views.frontend, name='frontend'),

    # Backend dashboard
    path('backend/', views.backend, name='backend'),

    # Patient operations
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient/<str:patient_id>/', views.patient, name='patient'),
    path('edit_patient/', views.edit_patient, name='edit_patient'),
    path('delete_patient/<str:patient_id>/', views.delete_patient, name='delete_patient'),
]

# Serve media/static files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
