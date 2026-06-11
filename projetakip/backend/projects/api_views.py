from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, ProjectGrade, Task, TaskProgress
from .serializers import (
    ProjectGradeSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    TaskProgressSerializer,
    TaskSerializer,
)
from core.permissions import IsTeacher

from .services import check_completion_threshold, ensure_task_progress, update_project_status


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Project.objects.filter(teacher=user)
        return user.student_projects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.query_params.get('simple'):
            return ProjectListSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save(teacher=self.request.user)
        ensure_task_progress(project)


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Project.objects.filter(teacher=user)
        return user.student_projects.all()

    def perform_update(self, serializer):
        project = serializer.save()
        ensure_task_progress(project)
        update_project_status(project)


class ProjectCompleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def post(self, request, pk):
        project = Project.objects.filter(pk=pk, teacher=request.user).first()
        if not project:
            return Response({'detail': 'Proje bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        project.status = Project.Status.COMPLETED
        project.completed_at = timezone.now()
        project.save()
        return Response(ProjectSerializer(project).data)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Task.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'], teacher=self.request.user)
        task = serializer.save(project=project)
        ensure_task_progress(project)
        return task


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project__teacher=self.request.user)


class TaskProgressListAPIView(generics.ListAPIView):
    serializer_class = TaskProgressSerializer

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        qs = TaskProgress.objects.select_related('task', 'student')
        if project_id:
            qs = qs.filter(task__project_id=project_id)
        if user.is_student:
            qs = qs.filter(student=user)
        elif user.is_teacher:
            qs = qs.filter(task__project__teacher=user)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class TaskProgressUpdateAPIView(APIView):
    def post(self, request, pk, action):
        user = request.user
        progress = TaskProgress.objects.filter(pk=pk).select_related('task__project').first()
        if not progress:
            return Response({'detail': 'Kayıt bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        if user.is_student and progress.student != user:
            return Response({'detail': 'Yetkisiz.'}, status=status.HTTP_403_FORBIDDEN)
        if action == 'start':
            if progress.status == TaskProgress.Status.NOT_STARTED:
                progress.status = TaskProgress.Status.IN_PROGRESS
                progress.started_at = timezone.now()
                progress.save()
        elif action == 'complete':
            progress.status = TaskProgress.Status.COMPLETED
            progress.completed_at = timezone.now()
            if not progress.started_at:
                progress.started_at = timezone.now()
            progress.save()
            check_completion_threshold(progress.task.project)
        else:
            return Response({'detail': 'Geçersiz işlem.'}, status=status.HTTP_400_BAD_REQUEST)
        update_project_status(progress.task.project)
        return Response(TaskProgressSerializer(progress).data)


class GradeAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    serializer_class = ProjectGradeSerializer

    def get_object(self):
        project = Project.objects.get(pk=self.kwargs['project_pk'], teacher=self.request.user)
        student_id = self.kwargs['student_pk']
        grade, _ = ProjectGrade.objects.get_or_create(project=project, student_id=student_id)
        return grade


class LocationUpdateAPIView(APIView):
    """Mobil GPS konumunu projeye kaydet."""

    def post(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        if not project:
            return Response({'detail': 'Proje bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        if lat is None or lng is None:
            return Response({'detail': 'latitude ve longitude gerekli.'}, status=status.HTTP_400_BAD_REQUEST)
        project.location_lat = lat
        project.location_lng = lng
        project.save(update_fields=['location_lat', 'location_lng'])
        return Response({'detail': 'Konum kaydedildi.'})
