# views.py is a file that contains the views for the mainapp application.


from django.shortcuts import render, redirect  
from .forms import AddForm
from .models import User, Worker,Request, User
from django.contrib import messages  # ✅ Import messages for flash messages
from django.contrib.auth import authenticate   # ✅ Import authenticate and login
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import re
from django.shortcuts import get_object_or_404





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

def contactus(request):
    return render(request, 'contactus.html')  # Render plumbing.html

# worker registration------------------------------------------------>

def worker_register(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        confirm_password = make_password(request.POST.get('confirm_password'))
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        profession = request.POST.get('profession')
        experience = request.POST.get('experience')
        worker = Worker.objects.create(title=title,first_name=first_name,last_name=last_name,email=email,password=password,confirm_password=confirm_password,gender=gender,phone=phone,profession=profession,experience=experience)
        messages.success(request, "Registration successful! Please login.")
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(password_pattern, password):
            return redirect('worker_login')
    return render(request, 'worker_reg.html')
    return render(request, "worker_reg.html", {"error": "Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number. No spaces or underscores allowed."})

        
# worker login------------------------------------------------>


def worker_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            worker = Worker.objects.get(email=email)
            if check_password(password, worker.password):  # Verify hashed password
                request.session["worker_id"] = worker.id  # Store worker ID in session
                return redirect("worker_dashboard")
            else:
                return render(request, "worker_login.html", {"error": "Invalid password!"})
        except Worker.DoesNotExist:
            return render(request, "worker_login.html", {"error": "Worker not found!"})

    return render(request, "worker_login.html")

# worker dashboard------------------------------------------------>

@login_required
def worker_dashboard(request):
    worker_id = request.session.get("worker_id")
    if not worker_id:
        return redirect("worker_login")

    worker = Worker.objects.get(id=worker_id)
    
    # Fetch only accepted jobs
    jobs = Request.objects.filter(worker=worker, status="Accepted")
    
    return render(request, 'worker_dashboard.html', {'worker': worker, 'jobs': jobs})


# worker logout------------------------------------------------>

def worker_logout(request):
    request.session.flush()  # Clear worker session
    return redirect('worker_login')  # Redirect to worker login page

# worker request------------------------------------------------>


def worker_requests(request):
    if "worker_id" not in request.session:
        return redirect("worker_login")

    worker = Worker.objects.get(id=request.session["worker_id"])
    requests = Request.objects.filter(worker=worker, status="Pending")

    return render(request, "worker_requests.html", {"worker": worker, "requests": requests})

def update_request(request, request_id, action):
    request_obj = Request.objects.get(id=request_id)
    if action == "accept":
        request_obj.status = "Accepted"
    elif action == "reject":
        request_obj.status = "Rejected"
    request_obj.save()
    
    return redirect("worker_dashboard")



# user registration------------------------------------------------>


def user_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        city = request.POST["city"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"

        if not re.match(password_pattern, password):
            return render(request, "user_reg.html", {"error": "Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number. No spaces or underscores allowed."})

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, 'user_reg.html', {"error": "Email already registered!"})

        # Create a new user
        user = User(name=name, email=email, phone=phone, address=address, city=city, password=password, confirm_password=confirm_password)
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('user_login')

    return render(request, "user_reg.html")


# user login------------------------------------------------>

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            user = User.objects.get(email=email)
            if user.password == password:  # Implement proper password hashing
                request.session["user_id"] = user.id
                return redirect("user_dashboard")
            else:
                return render(request, "user_login.html", {"error": "Invalid credentials"})
        except User.DoesNotExist:
            return render(request, "user_login.html", {"error": "User not found"})

    return render(request, "user_login.html")



def user_dashboard(request):
    if "user_id" not in request.session:
        return redirect("user_login")

    user = User.objects.get(id=request.session["user_id"])
    
    # Get all unique professions from the Worker model
    professions = Worker.objects.values_list('profession', flat=True).distinct()
    
    # Get the selected profession from the request
    selected_profession = request.GET.get("profession", "")

    # Filter workers based on the selected profession
    if selected_profession:
        workers = Worker.objects.filter(profession=selected_profession)
    else:
        workers = Worker.objects.all()

    requests = Request.objects.filter(user=user)

    return render(request, "user_dashboard.html", {
        "user": user,
        "workers": workers,
        "requests": requests,
        "professions": professions,
        "selected_profession": selected_profession
    })










# user logout------------------------------------------------>

def user_logout(request):
    request.session.flush()  # Clear user session
    return redirect('user_login')  # Redirect to user login page


# user send request------------------------------------------------>


def send_request(request, worker_id):
    if "user_id" not in request.session:
        return redirect("user_login")

    user = User.objects.get(id=request.session["user_id"])
    worker = Worker.objects.get(id=worker_id)

    existing_request = Request.objects.filter(user=user, worker=worker, status="Pending").first()
    if existing_request:
        messages.warning(request, "You already have a pending request for this worker.")
        return redirect("user_dashboard")

    Request.objects.create(user=user, worker=worker)
    messages.success(request, "Request sent successfully!")
    return redirect("user_dashboard")




def view_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    return render(request, 'view_worker.html', {'worker': worker})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')



def complete_job(request, job_id):
    if "worker_id" not in request.session:
        return redirect("worker_login")

    job = get_object_or_404(Request, id=job_id)

    if job.worker.id == request.session["worker_id"]:  # Ensure only the assigned worker can complete the job
        job.status = "Completed"
        job.save()
        messages.success(request, "Job marked as completed successfully!")

    return redirect("worker_dashboard")