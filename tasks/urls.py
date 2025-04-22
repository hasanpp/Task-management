from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', UserTaskListView.as_view(), name='view_tasks'),
    path('<int:pk>/', UserTaskUpdateView.as_view(), name='tast_update'),
    path('<int:pk>/report/', TaskReportView.as_view(), name='tast_report'),
]