# admin.py


from django.contrib import admin
from .models import  User, Worker
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



admin.site.register(User)






class WorkerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'profession', 'is_approved', 'status')
    list_filter = ('is_approved', 'status', 'profession')
    search_fields = ('first_name', 'last_name', 'email', 'profession')

    actions = ['approve_worker', 'reject_worker']

    @admin.action(description="Approve selected workers")
    def approve_worker(self, request, queryset):
        for worker in queryset:
            if not worker.is_approved:
                worker.is_approved = True
                worker.save()

                # Send email confirmation to the worker
                subject = "🎉 Your Registration Has Been Approved!"
                message = f"""
                Dear {worker.first_name} {worker.last_name},

                Your registration on FIXIT has been approved by the admin.  
                You can now log in to your account and start accepting jobs.

                Best regards,  
                The FIXIT Team  
                """
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [worker.email],
                        fail_silently=False
                    )
                    messages.success(request, f"{worker.first_name} {worker.last_name} has been approved, and an email has been sent.")
                except Exception as e:
                    messages.error(request, f"Failed to send email to {worker.email}: {e}")

    @admin.action(description="Reject selected workers")
    def reject_worker(self, request, queryset):
        for worker in queryset:
            if not worker.is_approved:
                worker.delete()

                # Send email rejection to the worker
                subject = "❌ Your Registration Has Been Rejected"
                message = f"""
                Dear {worker.first_name} {worker.last_name},
                Unfortunately, your registration has been rejected by admin.
                
                Best regards,  
                The FIXIT Team 
                """
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [worker.email],
                        fail_silently=False
                    )
                    messages.success(request, f"{worker.first_name} {worker.last_name} has been rejected.")
                except Exception as e:
                    messages.error(request, f"Failed to send email to {worker.email}: {e}")
admin.site.register(Worker, WorkerAdmin)  # ✅ Correct

