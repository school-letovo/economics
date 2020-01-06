from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Problem
# Create your views here.

def all_problem_list(request):
    problems = Problem.objects.all()
    context = {'problems': problems,}
    return render(request, 'problems/problem_list.html', context)

def all_student_list(request):
    students = User.objects.all()
    context = {'students': students,}
    return render(request, 'problems/student_list.html', context)
