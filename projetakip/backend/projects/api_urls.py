from django.urls import path

from . import api_views

urlpatterns = [
    path('projects/', api_views.ProjectListCreateAPIView.as_view(), name='api_projects'),
    path('projects/<int:pk>/', api_views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
    path('projects/<int:pk>/complete/', api_views.ProjectCompleteAPIView.as_view(), name='api_project_complete'),
    path('projects/<int:pk>/location/', api_views.LocationUpdateAPIView.as_view(), name='api_project_location'),
    path('projects/<int:project_pk>/tasks/', api_views.TaskListCreateAPIView.as_view(), name='api_tasks'),
    path('tasks/<int:pk>/', api_views.TaskDetailAPIView.as_view(), name='api_task_detail'),
    path('projects/<int:project_pk>/progress/', api_views.TaskProgressListAPIView.as_view(), name='api_progress'),
    path('progress/', api_views.TaskProgressListAPIView.as_view(), name='api_all_progress'),
    path('progress/<int:pk>/<str:action>/', api_views.TaskProgressUpdateAPIView.as_view(), name='api_progress_action'),
    path(
        'projects/<int:project_pk>/grades/<int:student_pk>/',
        api_views.GradeAPIView.as_view(),
        name='api_grade',
    ),
]
