from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.all_problem_list, name='all_problem_list'),
    path('students', views.all_student_list, name='all_student_list'),
]