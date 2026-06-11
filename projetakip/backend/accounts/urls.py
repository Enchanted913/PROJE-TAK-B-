from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset/confirm/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('password-reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
]
