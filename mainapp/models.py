# models.py


from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now  # Ensure this import exists

# User Model-------------------------------->

class User(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,  unique=True)
    password = models.CharField(max_length=100)
    phone = models.BigIntegerField(unique=True)  # ✅ Change to BigIntegerField
    address = models.TextField(default="Not provided")
    city = models.CharField(max_length=100 ,default="Unknown")
    confirm_password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#worker model--------------------------------->
class Worker(models.Model):

    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='Mr')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Hashed password storage
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone = models.CharField(max_length=15)
    profession = models.TextField()
    experience = models.TextField()
    amount = models.TextField()
    status = models.BooleanField(default=True, )  # Worker availability
    is_approved = models.BooleanField(default=False)  # New field

    
    

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name} - {self.status}"


#request model------------------------------->
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'),('Completed', 'Completed') ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Request by {self.user.name} - {self.status}"

#notification model----------------------------->
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('accept', 'Accept'),
        ('reject', 'Reject'),
        ('complete', 'Complete'),
        ('request', 'Request'),
    ]
    worker_email = models.EmailField()  # Store the worker's email
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)  # Type of notification
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)