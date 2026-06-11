from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('pdf/', views.report_pdf, name='report_pdf'),
]
