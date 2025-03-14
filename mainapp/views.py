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
from django.db.models import Q
from django.urls import reverse





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
        
        # Save worker ID in session for payment reference
        request.session['worker_id'] = worker.id

        messages.success(request, "Registration successful! Please complete the payment.")
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(password_pattern, password):
            return redirect('payment')
    return render(request, 'worker_reg.html')
    return render(request, "worker_reg.html", {"error": "Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number. No spaces or underscores allowed."})

        


# Payment Page View
def payment(request):
    if 'worker_id' not in request.session:
        return redirect('worker_login')

    return render(request, 'payment.html')


# Process Payment
def process_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        worker_id = request.session.get('worker_id')

        if not worker_id:
            messages.error(request, "Session expired! Please register again.")
            return redirect('workerregister')
        
        # ✅ Add validation for card/UPI details (example)
        if payment_method == "Card":
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')

            if not (card_number and expiry_date and cvv):
                messages.error(request, "Invalid card details!")
                return redirect('payment')

        # ✅ UPI payment validation
        if payment_method == "UPI":
            upi_id = request.POST.get('upi_id')
            # Regex pattern for UPI ID validation
            upi_pattern = r'^[\w.-]+@[\w.-]+$'
            if not upi_id or not re.match(upi_pattern, upi_id):
                messages.error(request, "Invalid UPI ID format! Example: example@upi")
                return redirect('payment')


        # If payment is successful
        worker = Worker.objects.get(id=worker_id)
        worker.status = True  # Mark as available after payment
        worker.save()

        # Clear session after payment
        del request.session['worker_id']

        messages.success(request, "Payment successful! You can now log in.")
        return redirect('worker_login')

    return redirect('payment')









# worker login------------------------------------------------>


def worker_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            worker = Worker.objects.get(email=email)
            if check_password(password, worker.password):  # Verify hashed password
                request.session["worker_id"] = worker.id  # Store worker ID in session
                request.session["is_worker"] = True  # Add a flag to differentiate session
                messages.success(request, "Login successful!")
                return redirect("worker_dashboard")
            else:
                return render(request, "worker_login.html", {"error": "Invalid password!"})
        except Worker.DoesNotExist:
            return render(request, "worker_login.html", {"error": "Worker not found!"})

    return render(request, "worker_login.html")

# worker dashboard------------------------------------------------>

@login_required
def worker_dashboard(request):
    if "worker_id" not in request.session:
        return redirect("worker_login")

    worker = Worker.objects.get(id=request.session["worker_id"])
    
    # Fetch only accepted jobs
    jobs = Request.objects.filter(worker=worker, status="Accepted")
    
    return render(request, 'worker_dashboard.html', {'worker': worker, 'jobs': jobs})


# worker logout------------------------------------------------>

# def worker_logout(request):
#     request.session.flush()  # Clear worker session
#     return redirect('worker_login')  # Redirect to worker login page

def worker_logout(request):
    if "worker_id" in request.session:
        del request.session["worker_id"]  # Clear only worker session
    if "is_worker" in request.session:
        del request.session["is_worker"]  # Remove worker flag
    return redirect('worker_login')  # Redirect to worker login

# worker request------------------------------------------------>


def worker_requests(request):
    if "worker_id" not in request.session:
        return redirect("worker_login")

    worker = Worker.objects.get(id=request.session["worker_id"])
    requests = Request.objects.filter(worker=worker, status="Pending")

    return render(request, "worker_requests.html", {"worker": worker, "requests": requests})



# worker request update------------------------------------------------>
def update_request(request, request_id, action):
    request_obj = Request.objects.get(id=request_id)
    if action == "accept":
        request_obj.status = "Accepted"
        # Mark worker as not available when the job is accepted
        request_obj.worker.status = False
        request_obj.worker.save()
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
        login_input = request.POST["email"]  # Accept email or phone
        password = request.POST["password"]
            
        try:
            if login_input.isdigit():  # If input is numeric, treat it as phone
                user = User.objects.get(phone=login_input)
            else:
                user = User.objects.get(email=login_input)
                
            if user.password == password:  # ✅ Add password hashing if needed
                request.session["user_id"] = user.id
                messages.success(request, "Login successful!")
                return redirect("user_dashboard")
            else:
                return render(request, "user_login.html", {"error": "Invalid credentials"})
        except User.DoesNotExist:
            return render(request, "user_login.html", {"error": "User not found"})

    return render(request, "user_login.html")

# user_dashboard------------------------------------------------>

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


    # ✅ Check if the worker is available before sending request
    if not worker.status:
        messages.warning(request, "This worker is not available right now.")
        return redirect("user_dashboard")


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

# worker complete job------------------------------------------------>

def complete_job(request, job_id):
    if "worker_id" not in request.session:
        return redirect("worker_login")

    job = get_object_or_404(Request, id=job_id)

    if job.worker.id == request.session["worker_id"]:  # Ensure only the assigned worker can complete the job
        job.status = "Completed"
        job.save()
        messages.success(request, "Job marked as completed successfully!")

        # ✅ Set worker status back to available after job completion
        job.worker.status = True
        job.worker.save()

    return redirect("worker_dashboard")



# workeredit profile------------------------------------------------>

def edit_worker_profile(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)

    if request.method == 'POST':
        worker.first_name = request.POST['first_name']
        worker.last_name = request.POST['last_name']
        worker.email = request.POST['email']
        worker.phone = request.POST['phone']
        worker.save()
        return redirect('worker_dashboard')

    return render(request, 'edit_worker_profile.html', {'worker': worker})




