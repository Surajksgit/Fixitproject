# urls.py is a file that contains URL patterns for the mainapp application.


from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', views.home, name='home'),
    path('workerreg/', views.workerreg, name='workerreg'),
    path('workerregister/', views.worker_register, name='workerregister'),
    path('user_reg/', views.user_register, name='user_reg'),
    path('user_login/', views.user_login, name='user_login'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),  # About Page
    path('plumbing/', views.plumbing, name='plumbing'),  # New plumbing route
    path('electrician/', views.electrician, name='electrician'),  # New electrician route
    path('gardening/', views.gardening, name='gardening'),  # New gardening route
    path('cleaning/', views.cleaning, name='cleaning'),  # New gardening route
    path('painting/', views.painting, name='painting'),  # New gardening route
    path('contactus/', views.contactus, name='contactus'),  # New gardening route
    

    
]