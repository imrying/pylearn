from django.urls import path

from . import views

urlpatterns = [
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('student/joinclass/', views.student_join_class, name='student_join_class'),
    path('teacher/', views.teacher_view, name='teacher_view'),
    path('teacher/createclass', views.teacher_create_class, name='teacher_create_class'),
    path('teacher/createassignment', views.teacher_create_assignment, name='teacher_create_assignment'),
    path('student/', views.student_view, name='student_view'),
    path('', views.front_page, name='front_page_view'),
    path('teacher/<int:assignment_id>', views.single_class_view, name='single_class'),
    path('student/submit/<int:assignment_id>', views.submission_view, name="submission_view"),
    path('download/<str:path>', views.download, name="download_view"),
    path('student/<int:assignment_id>', views.assignment_view, name='assignmentview')
]