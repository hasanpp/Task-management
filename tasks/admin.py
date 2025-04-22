from django.contrib import admin
from .models import Task
from users.models import User

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date', 'worked_hours')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == User.SUPER_ADMIN):
            return qs
        elif hasattr(request.user, 'role') and request.user.role == User.ADMIN:
            return qs.filter(assigned_to__admin=request.user)
        return qs.filter(assigned_to=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to" and not request.user.is_superuser:
            if hasattr(request.user, 'role'):
                if request.user.role == User.ADMIN:
                    kwargs["queryset"] = User.objects.filter(admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)