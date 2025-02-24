# models.py


from django.db import models

# Create your models here.

# Custom User Model

class User(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=100,default="Not provided")
    address = models.TextField(default="Not provided")
    city = models.CharField(max_length=100 ,default="Unknown")
    

    def __str__(self):
        return self.name

# Worker Model

class Worker(models.Model):

    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        
    ]

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='Mr')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')] )
    phone = models.IntegerField()
    profession = models.TextField()
    

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"