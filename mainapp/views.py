# views.py is a file that contains the views for the mainapp application.


from django.shortcuts import render, redirect 
from .forms import AddForm
from .models import User, Worker,Request, User
from django.contrib import messages  # ✅ Import messages for flash messages
from django.contrib.auth import authenticate   # ✅ Import authenticate and login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import re
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os
from .models import Notification





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

# Worker Registration View
def worker_register(request):
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        profession = request.POST.get('profession')
        experience = request.POST.get('experience')
        amount = request.POST.get('amount')
        # ✅ Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('worker_register')

        # ✅ Validate password strength
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(password_pattern, password):
            messages.error(request, "Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one digit.")
            return redirect('worker_register')

        # ✅ Hash the password before saving
        hashed_password = make_password(password)

        worker = Worker.objects.create(title=title,first_name=first_name,last_name=last_name,email=email,password=make_password(password),gender=gender,phone=phone,profession=profession,experience=experience,amount=amount,is_approved=False)
        
        # Save worker ID in session for payment reference
        request.session['worker_id'] = worker.id

        # Stylish HTML email content with inline image
        subject = "🎉 Registration Successful - Pending Approval 🎉"
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        margin: 0;
                        padding: 0;
                        color: #333;
                    }}
                    .container {{
                        width: 100%;
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }}
                    h2 {{
                        color: #4CAF50;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.6;
                    }}
                    .footer {{
                        margin-top: 20px;
                        text-align: center;
                        font-size: 14px;
                        color: #888;
                    }}
                    img {{
                        display: block;
                        margin: 20px auto;
                        width: 100px;
                        height: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Welcome to <strong>FIXIT</strong>, {first_name}!</h2>
                    <p>Thank you for registering with <strong>FIXIT</strong>. Your account is currently pending approval by the admin.</p>
                    <p>You will receive another email once your account has been approved.</p>
                    <img src="cid:fixit_logo" alt="FIXIT Logo"/>
                    <p class="footer">Best regards,<br>
                    <strong>The FIXIT Team</strong></p>
                </div>
            </body>
        </html>
        """

        # Create EmailMessage instance
        email_message = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [email])
        email_message.content_subtype = 'html'

        # Attach the image inline
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'fixit_logo.png')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img:
                mime_image = MIMEImage(img.read(), _subtype="png")
                mime_image.add_header('Content-ID', '<fixit_logo>')
                mime_image.add_header('Content-Disposition', 'inline', filename='fixit_logo.png')
                email_message.attach(mime_image)

        # Send email
        email_message.send()

        messages.success(request, "Registration successful! Please complete the payment.")
        return redirect('payment')
    return render(request, 'worker_reg.html')


# worker Payment Page View----------------------------------->
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
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            worker = Worker.objects.get(email=email)
            if check_password(password, worker.password):  # Verify hashed password
                if worker.is_approved:  # Check if the worker is approved
                    request.session["worker_id"] = worker.id  # Store worker ID in session
                    request.session["is_worker"] = True  # Add a flag to differentiate session
                    messages.success(request, "Login successful!")
                    return redirect("worker_dashboard")
                else:
                    messages.error(request, "Your account is pending approval by the admin.")
                    return redirect("worker_login")
            else:
                messages.error(request, "Invalid password!")
                return redirect("worker_login")
        except Worker.DoesNotExist:
            messages.error(request, "Worker not found!")
            return redirect("worker_login")

    return render(request, "worker_login.html")
    
# worker dashboard------------------------------------------------>

@login_required
def worker_dashboard(request):
    worker_id = request.session.get("worker_id")
    if not worker_id:
        messages.error(request, "You are not logged in as a worker.")
        return redirect("worker_login")
    
    try:
        worker = Worker.objects.get(id=worker_id)  # Fetch the Worker instance using session
        jobs = Request.objects.filter(worker=worker, status="Accepted")  # Filter accepted jobs
        return render(request, 'worker_dashboard.html', {'worker': worker, 'jobs': jobs})
    except Worker.DoesNotExist:
        messages.error(request, "Worker not found.")
        return redirect("worker_login")

# worker logout------------------------------------------------>


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

        # ✅ Create notification for worker using worker's email
        Notification.objects.create(
            worker_email=request_obj.worker.email,  # Use the worker's email
            message=f"Your work request has been accepted by {request_obj.worker.first_name}."
        )


        subject = "Your Work Request Was Accepted"
        message = f"Hello {request_obj.user.name},\n\nYour work request has been accepted by {request_obj.worker.first_name}. They will contact you soon!"
        send_mail(subject, message, "fixit1361@gmail.com", [request_obj.user.email])


    elif action == "reject":
        request_obj.status = "Rejected"

        # ✅ Create notification for worker using worker's email
        Notification.objects.create(
            worker_email=request_obj.worker.email,  # Use the worker's email
            message=f"Unfortunately, {request_obj.worker.first_name} has rejected your work request."
        )

        subject = "Your Work Request Was Rejected"
        message = f"Hello {request_obj.user.name},\n\nUnfortunately, {request_obj.worker.first_name} has rejected your work request. You can try requesting another worker."
        send_mail(subject, message, "fixit1361@gmail.com", [request_obj.user.email])


    elif action == "completed":
        request_obj.status = "Completed"
        request_obj.worker.status = True  # Mark worker as available again
        request_obj.worker.save()

        # ✅ Create notification for worker using worker's email
        Notification.objects.create(
            worker_email=request_obj.worker.email,  # Use the worker's email
            message=f"Your work request handled by {request_obj.worker.first_name} has been marked as completed."
        )

        subject = "Work Completed Successfully"
        message = f"Hello {request_obj.user.name},\n\nYour work request handled by {request_obj.worker.first_name} has been marked as completed. Thank you for using FixIt!"
        send_mail(subject, message, "fixit1361@gmail.com", [request_obj.user.email])




    request_obj.save()
    
    return redirect("worker_dashboard")

# DONT TOUCH THE BELOW CODE---------------------------------->
# Approve Worker View----------------------------------->
@staff_member_required
def approve_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.status = 'approved'
    worker.save()

    # Notify Worker via Email (Plain Text)
    subject = "Registration Approved"
    message = f"Dear {worker.first_name},\n\nYour registration has been approved! You can now log in to your account.\n\nBest Regards,\nYour Team"
    send_mail(subject, message, "abhirampashok1@gmail.com", [worker.email], fail_silently=False)

    messages.success(request, f"Worker {worker.first_name} {worker.last_name} has been approved.")
    return redirect('admin_dashboard')

# Reject Worker View------------------------------>
@staff_member_required
def reject_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    worker.status = 'rejected'
    worker.save()

    # Notify Worker via Email (Plain Text)
    subject = "Registration Rejected"
    message = f"Dear {worker.first_name},\n\nUnfortunately, your registration has been rejected.\n\nBest Regards,\nYour Team"
    send_mail(subject, message, "abhirampashok1@gmail.com", [worker.email], fail_silently=False)

    messages.success(request, f"Worker {worker.first_name} {worker.last_name} has been rejected.")
    return redirect('admin_dashboard')

# DONT TOUCH THE ABOVE CODE---------------------------------->


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

        subject = "Welcome to FIXIT!"
        message = f"Hello {name},\n\nYour registration was successful. Welcome to FIXIT!\n\nBest Regards,\nThe Fixit Team"
        from_email = "fixit1361@gmail.com"
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, "Registration successful! Please login.")
        return redirect('user_login')

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

    
    # Get all notifications for the user
    requests = Request.objects.filter(user=user)

    # Get notifications for workers associated with the user's requests
    worker_emails = requests.values_list('worker__email', flat=True)
    notifications = Notification.objects.filter(worker_email__in=worker_emails).order_by('-created_at')[:10]
    

    return render(request, "user_dashboard.html", {
        "user": user,
        "workers": workers,
        "requests": requests,
        "professions": professions,
        "selected_profession": selected_profession,
        "notifications": notifications
    })


# user logout------------------------------------------------>

def user_logout(request):
    request.session.pop("user_id", None)  # Remove only the user session key
    return redirect('user_login')


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

    # ✅ Create notification for worker using worker's email
    Notification.objects.create(
        worker_email=worker.email,  # Store the worker's email
        message=f"You have a new work request from {user.name}."
    )

    subject = "New Work Request Received"
    message = f"Hello {worker.first_name},\n\nYou have received a new work request from {user.name}.\n\nPlease check your dashboard for more details."
    send_mail(subject, message, "fixit1361@gmail.com", [worker.email])




    messages.success(request, "Request sent successfully!")
    return redirect("user_dashboard")


# view worker------------------------------------------------>

def view_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    return render(request, 'view_worker.html', {'worker': worker})

# privacy policy------------------------------------------------>

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

# notification------------------------------------------------>
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.user == request.user:
        notification.is_read = True
        notification.save()
    return redirect('user_dashboard')







