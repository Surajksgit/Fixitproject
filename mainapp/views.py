# views.py is a file that contains the views for the mainapp application.


from django.shortcuts import render, redirect  
from .forms import AddForm
from .models import User, Worker
from django.contrib import messages  # ✅ Import messages for flash messages
from django.contrib.auth import authenticate   # ✅ Import authenticate and login



# Create your views here.
def home(request):
    return render(request, 'home.html')

def workerreg(request):
    return render(request, 'worker_reg.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')


def plumbing(request):
    return render(request, 'plumbing.html')  # Render plumbing.html


def electrician(request):
    return render(request, 'electrician.html')  # Render plumbing.html

def gardening(request):
    return render(request, 'gardening.html')  # Render plumbing.html

def cleaning(request):
    return render(request, 'cleaning.html')  # Render plumbing.html


def painting(request):
    return render(request, 'painting.html')  # Render plumbing.html



def worker_register(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        profession = request.POST.get('profession')
        Worker(title=title,first_name=first_name,last_name=last_name,email=email,password=password,gender=gender,phone=phone,profession=profession).save()
    return redirect('home')  
    return render(request, 'worker_reg.html')


def user_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        city = request.POST["city"]
        password = request.POST["password"]

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, 'user_reg.html', {"error": "Email already registered!"})

        # Create a new user
        user = User(name=name, email=email, phone=phone, address=address, city=city, password=password)
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('user_login')

    return render(request, "user_reg.html")




def user_login(request):
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]
        
        user = authenticate(request, name=name, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home page after login
        else:
            return render(request, "user_login.html", {"error": "Invalid username or password"})

    return render(request, "user_login.html")