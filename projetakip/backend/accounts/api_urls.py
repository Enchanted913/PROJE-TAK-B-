from django.urls import path

from . import api_views

urlpatterns = [
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('profile/', api_views.ProfileAPIView.as_view(), name='api_profile'),
    path('fcm-token/', api_views.FCMTokenAPIView.as_view(), name='api_fcm_token'),
    path('students/', api_views.StudentListCreateAPIView.as_view(), name='api_students'),
    path('students/<int:pk>/', api_views.StudentDetailAPIView.as_view(), name='api_student_detail'),
]
