from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Assignment, Problem
from datetime import datetime

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

def index(request):
    students = User.objects.all()
    problems = Problem.objects.all()
    context = {'problems': problems,
               'students': students,}
    return render(request, 'problems/sb/index.html', context)

def assign(request):
    if request.POST['date_deadline']:
        date_deadline = datetime.strptime(request.POST['date_deadline'], "%Y-%m-%d")
    else:
        date_deadline = None
    for student in request.POST.getlist('student'):
        for problem in request.POST.getlist('problem'):
            assign_task = Assignment(person=User.objects.get(id=int(student)), problem=Problem.objects.get(id=int(problem)), date_deadline=date_deadline, assigned_by=request.user).save()
    return redirect('index')

