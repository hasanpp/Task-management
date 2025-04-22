from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'admin')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superadmin = request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == User.SUPER_ADMIN)
        
        if not is_superadmin:
            if 'role' in form.base_fields:
                form.base_fields['role'].disabled = True
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == User.SUPER_ADMIN):
            return qs
        return qs.filter(admin=request.user)
