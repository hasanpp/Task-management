from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer

class UserTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            tasks = Task.objects.filter(assigned_to=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"message": str(e)}, status=409)
       
class UserTaskUpdateView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.assigned_to != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        status_val = request.data.get('status')
        if status_val == 'Completed':
            if not request.data.get('completion_report') or not request.data.get('worked_hours'):
                return Response({'error': 'Completion report and worked hours required when completing a task.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)
    
class TaskReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({'error': 'Only Admins or SuperAdmins can access this.'},
                            status=status.HTTP_403_FORBIDDEN)

        if task.status != 'completed':
            return Response({'error': 'Task is not completed yet.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskReportSerializer(task)
        return Response(serializer.data)