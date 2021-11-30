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
    path('', views.front_page, name='front_page_view')

]