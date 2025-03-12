# urls.py is a file that contains URL patterns for the mainapp application.


from django.urls import path
from . import views
from .views import home, worker_logout , user_dashboard, send_request,edit_worker_profile,edit_profile,profile_view

urlpatterns = [
    path('', views.home, name='home'),
    path('workerregister/', views.worker_register, name='workerregister'),
    path('worker_dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path("worker/login/", views.worker_login, name="worker_login"),
    path('worker/logout/', worker_logout, name='worker_logout'),
    path('user_reg/', views.user_register, name='user_reg'),
    path('user_login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),  # About Page
    path('plumbing/', views.plumbing, name='plumbing'),  # New plumbing route
    path('electrician/', views.electrician, name='electrician'),  # New electrician route
    path('gardening/', views.gardening, name='gardening'),  # New gardening route
    path('cleaning/', views.cleaning, name='cleaning'),  # New cleaning route
    path('painting/', views.painting, name='painting'),  # New painting route
    path('contactus/', views.contactus, name='contactus'),  # New contactus route
    path("user_dashboard/", user_dashboard, name="user_dashboard"),
    path("send_request/<int:worker_id>/", send_request, name="send_request"),
    path("worker_requests/", views.worker_requests, name="worker_requests"),
    path("update_request/<int:request_id>/<str:action>/", views.update_request, name="update_request"),
    path('worker/<int:worker_id>/', views.view_worker, name='view_worker'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('complete-job/<int:job_id>/', views.complete_job, name='complete_job'),
    path('worker/edit/<int:worker_id>/', edit_worker_profile, name='edit_worker_profile'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),


]