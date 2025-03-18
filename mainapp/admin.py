# admin.py


from django.contrib import admin
from .models import  User, Worker

admin.site.register(User)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'profession', 'status')
    list_filter = ('status',)
    actions = ['approve_workers', 'reject_workers']

    def approve_workers(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected workers have been approved.")

    def reject_workers(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected workers have been rejected.")

admin.site.register(Worker, WorkerAdmin)