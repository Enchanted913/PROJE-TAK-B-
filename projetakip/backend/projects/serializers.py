from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer

from .models import Project, ProjectGrade, Task, TaskProgress


class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'project', 'title', 'description', 'due_date', 'order', 'is_overdue')


class TaskProgressSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_color = serializers.CharField(read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskProgress
        fields = (
            'id', 'task', 'task_title', 'student', 'student_name',
            'status', 'status_display', 'status_color',
            'started_at', 'completed_at',
        )
        read_only_fields = ('student',)

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username


class ProjectGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = ProjectGrade
        fields = ('id', 'project', 'student', 'student_name', 'score', 'note')

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username


class ProjectSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.filter(role=User.Role.STUDENT),
        write_only=True, source='students', required=False,
    )
    tasks = TaskSerializer(many=True, read_only=True)
    completion_percentage = serializers.FloatField(read_only=True)
    completed_task_count = serializers.IntegerField(read_only=True)
    total_task_count = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'teacher', 'students', 'student_ids',
            'status', 'status_display', 'created_at', 'completed_at',
            'location_lat', 'location_lng', 'tasks',
            'completion_percentage', 'completed_task_count', 'total_task_count',
        )
        read_only_fields = ('teacher', 'completed_at')


class ProjectListSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.FloatField(read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'status', 'created_at', 'completion_percentage', 'student_count',
        )

    def get_student_count(self, obj):
        return obj.students.count()
