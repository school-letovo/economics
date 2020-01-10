from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.defaults import page_not_found

from .models import Assignment, Problem

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
    if request.user.groups.filter(name='teachers').exists():
        students = User.objects.all()
        problems = Problem.objects.all()
        context = {'problems': problems,
                   'students': students,}
        return render(request, 'problems/sb/index_teacher.html', context)
    elif request.user.groups.filter(name='students').exists():
        assigned_problems = Assignment.objects.filter(person=request.user).order_by('date_deadline')
        context = {'assigned_problems': assigned_problems,}
        return render(request, 'problems/sb/index_student.html', context)
    else:
        return render(request, 'problems/sb/login.html', {})

def assign(request):
    if request.POST['date_deadline']:
        date_deadline = datetime.strptime(request.POST['date_deadline'], "%Y-%m-%d")
    else:
        date_deadline = None
    for student in request.POST.getlist('student'):
        for problem in request.POST.getlist('problem'):
            assign_task = Assignment(person=User.objects.get(id=int(student)), problem=Problem.objects.get(id=int(problem)), date_deadline=date_deadline, assigned_by=request.user).save()
    return redirect('index')

