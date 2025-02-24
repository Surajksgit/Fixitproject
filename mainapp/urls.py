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

    
]