from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from .models import Assignment, Problem, Topic, Submit, Source
from .forms import SubmitForm, CheckForm

# Create your views here.

def index(request):
    if request.user.groups.filter(name='teachers').exists():
        students = User.objects.filter(groups__name='students')
        topics = Topic.objects.all()
        problems = dict()
        groups = Group.objects.all()
        for topic in topics:
            problems[topic.id] = topic.problems.all()
        topic = Topic.objects.get(id=1)
        submits = Submit.objects.filter(assignment__assigned_by=request.user).filter(verdict=-1) # solution not checked
        context = {'problems': problems,
                   'students': students,
                   'topic': topic,
                   'submits': submits,
                   'groups': groups,}
        return render(request, 'problems/sb/index_teacher.html', context)
    elif request.user.groups.filter(name='students').exists():
        assigned_problems = Assignment.objects.filter(person=request.user).order_by('status', 'date_deadline')
        form = SubmitForm()
        context = {'assigned_problems': assigned_problems, 'form': form}
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
    for group_id in request.POST.getlist('group'):
        group = Group.objects.get(id=group_id)
        print(group)
        print(group.user_set.all())
        for student in group.user_set.all():
            for problem in request.POST.getlist('problem'):
                assign_task = Assignment(person=student, problem=Problem.objects.get(id=int(problem)), date_deadline=date_deadline, assigned_by=request.user).save()
    return redirect('index')

def submit(request):
    assignment = Assignment.objects.get(id=request.POST["assignment_id"])
    Submit(assignment=assignment, short_answer=request.POST["short_answer"], solution=request.POST["solution"]).save()
    assignment.status = 1
    assignment.save()
    return redirect("index")

def check_solution(request, submit_id):
    submit = Submit.objects.get(id=submit_id)
    if request.user == submit.assignment.assigned_by:
        form = CheckForm()
        context = {'form': form, 'submit': submit}
        return render(request, 'problems/sb/index_temp.html', context)
    else:
        return redirect('index')

def save_verdict(request):
    verdict = request.POST['verdict']
    teacher_comment = request.POST['teacher_comment']
    submit_id = request.POST['submit_id']
    submit = Submit.objects.get(id=submit_id)
    submit.verdict = verdict
    submit.teacher_comment = teacher_comment
    submit.assignment.status = 2 # assignment solution checked
    submit.save()
    submit.assignment.save()
    return redirect('index')

def test(request):
    topic = Source.objects.get(id=22)
    return render(request, 'problems/test.html', {'topic_list':{topic}})

def source_list(request):
    source_ids = list(map(int, request.POST.getlist('source')))
    for source_id in source_ids:
        for child in Source.objects.get(id=source_id).children.all():
            source_ids.append(child.id)
        if not Source.objects.get(id=source_id).children.all():
            print(Source.objects.get(id=source_id).problem)
    print(source_ids)
    print(request.POST.getlist('source'))
    return render(request, 'problems/test.html', {})

