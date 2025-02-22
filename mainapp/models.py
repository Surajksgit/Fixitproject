from django.db import models

# Create your models here.

# Custom User Model

class User(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

# Worker Model

class Worker(models.Model):
    
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    skills = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name