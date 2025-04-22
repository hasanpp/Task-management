from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views as admin_views
from users import views as auth_views


urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', admin_views.admin_logout, name='logout'),
    path('', login_required(admin_views.admin_dashboard), name='admin_dashboard'),
    path('',admin_views.admin_dashboard, name='admin_dashboard'),
    path('users/', admin_views.admin_users, name='admin_users'),
    path('users/add/', admin_views.admin_add_user, name='admin_add_user'),
    path('users/<int:user_id>/edit/', admin_views.admin_edit_user, name='admin_edit_user'),
    path('users/<int:user_id>/delete/', admin_views.admin_delete_user, name='admin_delete_user'),
    path('admins/', admin_views.admin_admins, name='admin_admins'),
    path('admins/add/', admin_views.admin_add_admin, name='admin_add_admin'),
    path('admins/<int:admin_id>/demote/', admin_views.admin_demote_admin, name='admin_demote_admin'),
    path('admins/<int:admin_id>/delete/', admin_views.admin_delete_admin, name='admin_delete_admin'),
    path('admins/<int:admin_id>/assign-user/', admin_views.admin_assign_user, name='admin_assign_user'),
    path('admin_tasks/', admin_views.admin_tasks, name='admin_tasks'),
    path('admin_tasks/add/', admin_views.admin_add_task, name='admin_add_task'),
    path('admin_tasks/<int:task_id>/edit/', admin_views.admin_edit_task, name='admin_edit_task'),
    path('admin_tasks/<int:task_id>/delete/', admin_views.admin_delete_task, name='admin_delete_task'),
    path('task-reports/', admin_views.admin_task_reports, name='admin_task_reports'),
]