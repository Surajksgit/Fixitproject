# urls.py is a file that contains URL patterns for the mainapp application.


from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', views.home, name='home'),
    path('workerregister/', views.worker_register, name='workerregister'),
    path('worker_dashboard/<int:worker_id>/', views.worker_dashboard, name='worker_dashboard'),
    path('user_reg/', views.user_register, name='user_reg'),
    path('user_login/', views.user_login, name='user_login'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),  # About Page
    path('plumbing/', views.plumbing, name='plumbing'),  # New plumbing route
    path('electrician/', views.electrician, name='electrician'),  # New electrician route
    path('gardening/', views.gardening, name='gardening'),  # New gardening route
    path('cleaning/', views.cleaning, name='cleaning'),  # New cleaning route
    path('painting/', views.painting, name='painting'),  # New painting route
    path('contactus/', views.contactus, name='contactus'),  # New contactus route
    

    
]