"""
Author: Keerthana Thangavelu (C0932267)
Description: This file contains the urls for the 'students' app.
"""
from django.urls import path
from . import views
from .views import download_s3_file

urlpatterns = [
    path('', views.student_list, name='student_list'),
    # Route to the student list view; displays a list of all students.
    path('<int:pk>/', views.student_detail, name='student_detail'),
    # Route to the student detail view; displays details of a specific student identified by primary key (pk).
    path('new/', views.student_create, name='student_create'),
    # Route to the student creation view; allows creation of a new student.
    path('<int:pk>/edit/', views.student_update, name='student_update'),
    # Route to the student update view; allows updating of an existing student identified by primary key (pk).
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    # Route to the student deletion view; allows deletion of a student identified by primary key (pk).
    path('download/', views.download_report, name='download_report'),
    # Route to the download report view; allows downloading a report of students filtered by grade.
    path('download_s3_file/<path:file_key>/', views.download_s3_file, name='download_s3_file'),
]
