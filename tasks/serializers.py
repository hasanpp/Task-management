from rest_framework import serializers
from users.serializers  import UserSerializer
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 
                 'status', 'completion_report', 'worked_hours', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate(self, data):
        if 'status' in data and data['status'] == Task.STATUS_COMPLETED:
            if 'completion_report' not in data or not data['completion_report']:
                raise serializers.ValidationError(
                    {"completion_report": "Completion report is required when marking a task as completed."})
            if 'worked_hours' not in data or data['worked_hours'] is None:
                raise serializers.ValidationError(
                    {"worked_hours": "Worked hours is required when marking a task as completed."})
        return data


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report') or data.get('worked_hours') is None:
                raise serializers.ValidationError("Completion report and worked hours are required when marking task as completed.")
        return data
    
class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    
    def validate(self, data):
        if data['status'] == Task.STATUS_COMPLETED:
            if not data.get('completion_report'):
                raise serializers.ValidationError(
                    {"completion_report": "Completion report is required when marking a task as completed."})
            if not data.get('worked_hours'):
                raise serializers.ValidationError(
                    {"worked_hours": "Worked hours is required when marking a task as completed."})
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'assigned_to', 'completion_report', 'worked_hours', 'updated_at']
        read_only_fields = ['id', 'title', 'assigned_to', 'completion_report', 'worked_hours', 'updated_at']
