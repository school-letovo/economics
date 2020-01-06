from django.shortcuts import render

from .models import Problem
# Create your views here.

def all_problem_list(request):
    problems = Problem.objects.all()
    context = {'problems': problems,}
    return render(request, 'problems/problem_list.html', context)
