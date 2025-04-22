from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.db.models import Count
from functools import wraps
from users.models import User
from tasks.models import Task
from email_validator import validate_email, EmailNotValidError
from django.db.models import Q


def superadmin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role != User.SUPER_ADMIN:
            return HttpResponseForbidden("You don't have permission to access this page")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or (request.user.role != User.ADMIN and request.user.role != User.SUPER_ADMIN):
            return HttpResponseForbidden("You don't have permission to access this page")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
def admin_logout(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'role') or (request.user.role != User.ADMIN and request.user.role != User.SUPER_ADMIN):
        return HttpResponseForbidden("You don't have permission to access this page")
    
    # Get task statistics
    if request.user.role == User.SUPER_ADMIN:
        tasks = Task.objects.all()
        users = User.objects.all()
    else:  # Admin
        users = User.objects.filter(admin=request.user)
        tasks = Task.objects.filter(assigned_to__admin=request.user)
    
    context = {
        'total_tasks': tasks.count(),
        'pending_tasks': tasks.filter(status=Task.STATUS_PENDING).count(),
        'in_progress_tasks': tasks.filter(status=Task.STATUS_IN_PROGRESS).count(),
        'completed_tasks': tasks.filter(status=Task.STATUS_COMPLETED).count(),
        'recent_completed_tasks': tasks.filter(status=Task.STATUS_COMPLETED).order_by('-updated_at')[:5],
        'total_users': users.count(),
        'admin_count': users.filter(role=User.ADMIN).count(),
        'user_count': users.filter(role=User.USER).count(),
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@superadmin_required
def admin_users(request):
    users = User.objects.all()
    admins = User.objects.filter(role=User.ADMIN)
    
    context = {
        'users': users,
        'admins': admins,
    }
    
    return render(request, 'admin_panel/users.html', context)

@login_required
@superadmin_required
def admin_add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        admin_id = request.POST.get('admin')
        
        if len(username.replace(" ","")) == 0 or not username:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        if len(email.replace(" ","")) == 0 or not email:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')

        
        if len(role.replace(" ","")) == 0 or not role:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        try:
            emailinfo = validate_email(email)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            messages.error(request, str(e))
            return redirect('admin_users')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password, role=role)
            
            if role == User.USER and admin_id:
                admin = User.objects.get(id=admin_id, role=User.ADMIN)
                user.admin = admin
                user.save()
                
            messages.success(request, f"User {username} created successfully.")
            return redirect('admin_users')
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect('admin_users')
    
    return redirect('admin_users')

@login_required
@superadmin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        admin_id = request.POST.get('admin')
        
        if len(username.replace(" ","")) == 0 or not username:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        if len(email.replace(" ","")) == 0 or not email:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')

        
        if len(role.replace(" ","")) == 0 or not role:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        try:
            emailinfo = validate_email(email)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            messages.error(request, str(e))
            return redirect('admin_users')
        
        user.username = username
        user.email = email
        user.role = role
        
        if role == User.USER and admin_id:
            admin = User.objects.get(id=admin_id, role=User.ADMIN)
            user.admin = admin
        else:
            user.admin = None
        
        user.save()
        messages.success(request, f"User {username} updated successfully.")
        return redirect('admin_users')
    
    return redirect('admin_users')

@login_required
@superadmin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully.")
    
    return redirect('admin_users')

@login_required
@superadmin_required
def admin_admins(request):
    admins = User.objects.filter(role=User.ADMIN)
    all_users = User.objects.filter(role=User.USER)
    assignable_users = {}
    for admin in admins:
        admin.assignable_users = all_users.filter(Q(admin__isnull=True) | Q(admin=admin))

    context = { 'admins': admins, 'assignable_users': assignable_users, }
    
    return render(request, 'admin_panel/admins.html', context)



@login_required
@superadmin_required
def admin_add_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(username.replace(" ","")) == 0 or not username:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        if len(email.replace(" ","")) == 0 or not email:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        if len(password.replace(" ","")) == 0 or not email:
            messages.error(request, f"Username can't be none or empty.")
            return redirect('admin_users')
        
        try:
            emailinfo = validate_email(email)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            messages.error(request, str(e))
            return redirect('admin_users')
        
        try:
            User.objects.create_user(username=username, email=email, password=password, role=User.ADMIN)
            messages.success(request, f"Admin {username} created successfully.")
            return redirect('admin_admins')
        except Exception as e:
            messages.error(request, f"Error creating admin: {str(e)}")
            return redirect('admin_admins')
    
    return redirect('admin_admins')

@login_required
@superadmin_required
def admin_demote_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, role=User.ADMIN)
    
    if request.method == 'POST':
        admin.role = User.USER
        admin.save()
        
        new_admin_id = request.POST.get('new_admin')
        if new_admin_id:
            new_admin = get_object_or_404(User, id=new_admin_id, role=User.ADMIN)
            User.objects.filter(admin=admin).update(admin=new_admin)
        else:
            User.objects.filter(admin=admin).update(admin=None)
        
        messages.success(request, f"Admin {admin.username} demoted to user successfully.")
    
    return redirect('admin_admins')

@login_required
@superadmin_required
def admin_delete_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, role=User.ADMIN)
    
    if request.method == 'POST':
        # Reassign users previously assigned to this admin
        new_admin_id = request.POST.get('new_admin')
        if new_admin_id:
            new_admin = get_object_or_404(User, id=new_admin_id, role=User.ADMIN)
            User.objects.filter(admin=admin).update(admin=new_admin)
        else:
            User.objects.filter(admin=admin).update(admin=None)
        
        username = admin.username
        admin.delete()
        messages.success(request, f"Admin {username} deleted successfully.")
    
    return redirect('admin_admins')
@login_required
@superadmin_required
def admin_assign_user(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, role=User.ADMIN)

    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('users')
        User.objects.filter(admin=admin).update(admin=None)
        if selected_user_ids:
            User.objects.filter(id__in=selected_user_ids).update(admin=admin)
        messages.success(request, f"Users successfully updated for {admin.username}.")

    return redirect('admin_admins')


@login_required
@admin_required
def admin_tasks(request):
    # Get users based on role
    if request.user.role == User.SUPER_ADMIN:
        users = User.objects.filter(role=User.USER)
        tasks = Task.objects.all().select_related('assigned_to')
    else:  # Admin
        users = User.objects.filter(admin=request.user, role=User.USER)
        tasks = Task.objects.filter(assigned_to__admin=request.user).select_related('assigned_to')
    
    context = {
        'tasks': tasks,
        'users': users,
    }
    
    return render(request, 'admin_panel/tasks.html', context)

@login_required
@admin_required
def admin_add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        
        # Check if the user is under this admin's management (if admin)
        if request.user.role == User.ADMIN and assigned_to.admin != request.user:
            messages.error(request, "You can only assign tasks to users under your management.")
            return redirect('admin_tasks')
        
        task = Task(
            title=title,
            description=description,
            assigned_to=assigned_to,
            created_by=request.user,
            due_date=due_date,
            status=status
        )
        
        # If task is being created as completed, add completion report and worked hours
        if status == Task.STATUS_COMPLETED:
            completion_report = request.POST.get('completion_report')
            worked_hours = request.POST.get('worked_hours')
            
            if not completion_report or not worked_hours:
                messages.error(request, "Completion report and worked hours are required for completed tasks.")
                return redirect('admin_tasks')
            
            task.completion_report = completion_report
            task.worked_hours = worked_hours
        
        task.save()
        messages.success(request, f"Task '{title}' created successfully.")
        return redirect('admin_tasks')
    
    return redirect('admin_tasks')

@login_required
@admin_required
def admin_edit_task(request, task_id):
    # Get task and check permissions
    if request.user.role == User.SUPER_ADMIN:
        task = get_object_or_404(Task, id=task_id)
    else:  # Admin
        task = get_object_or_404(Task, id=task_id, assigned_to__admin=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')
        
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        
        # Check if the user is under this admin's management (if admin)
        if request.user.role == User.ADMIN and assigned_to.admin != request.user:
            messages.error(request, "You can only assign tasks to users under your management.")
            return redirect('admin_tasks')
        
        task.title = title
        task.description = description
        task.assigned_to = assigned_to
        task.due_date = due_date
        
        # If task status is changing to completed, ensure completion report and worked hours
        if status == Task.STATUS_COMPLETED and task.status != Task.STATUS_COMPLETED:
            completion_report = request.POST.get('completion_report')
            worked_hours = request.POST.get('worked_hours')
            
            if not completion_report or not worked_hours:
                messages.error(request, "Completion report and worked hours are required for completed tasks.")
                return redirect('admin_tasks')
            
            task.completion_report = completion_report
            task.worked_hours = worked_hours
        
        task.status = status
        task.save()
        
        messages.success(request, f"Task '{title}' updated successfully.")
        return redirect('admin_tasks')
    
    return redirect('admin_tasks')

@login_required
@admin_required
def admin_delete_task(request, task_id):
    # Get task and check permissions
    if request.user.role == User.SUPER_ADMIN:
        task = get_object_or_404(Task, id=task_id)
    else:  # Admin
        task = get_object_or_404(Task, id=task_id, assigned_to__admin=request.user)
    
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted successfully.")
    
    return redirect('admin_tasks')

@login_required
@admin_required
def admin_task_reports(request):
    # Get completed tasks based on role
    if request.user.role == User.SUPER_ADMIN:
        completed_tasks = Task.objects.filter(status=Task.STATUS_COMPLETED).select_related('assigned_to')
    else:  # Admin
        completed_tasks = Task.objects.filter(
            status=Task.STATUS_COMPLETED, 
            assigned_to__admin=request.user
        ).select_related('assigned_to')
    
    context = {
        'completed_tasks': completed_tasks,
    }
    
    return render(request, 'admin_panel/task_reports.html', context)
    
    