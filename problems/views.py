from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.views.generic.detail import DetailView
from django.contrib.auth.hashers import make_password

import economics.settings


from .models import Assignment, Problem, Topic, Submit, Source
from .forms import SubmitForm, CheckForm

# Create your views here.

SOURCE_ROOT = 22
TOPIC_ROOT = 1


def index(request):
    if request.user.groups.filter(name='teachers').exists():
        probs, tests, cases = filter_problems(request)
        students = User.objects.filter(groups__name='students')
        groups = Group.objects.all()
        topic = Topic.objects.get(id=TOPIC_ROOT)
        topic_list = tree2List(topic, count_problems_by_topic())
        source = Source.objects.get(id=SOURCE_ROOT)
        source_list = tree2List(source, count_problems_by_source())
        submits = Submit.objects.filter(assignment__assigned_by=request.user).filter(verdict=-1)  # solution not checked
        context = {'problems': probs,
                   'tests': tests,
                   'cases': cases,
                   'students': students,
                   'topic_list': topic_list,
                   'source_list': source_list,
                   'submits': submits,
                   'groups': groups,
                   }
        return render(request, 'problems/sb/index_teacher.html', context)

    elif request.user.groups.filter(name='students').exists():
        assigned_problems = Assignment.objects.filter(person=request.user).order_by('status', 'date_deadline')
        for assignment in assigned_problems:
            assignment.form = SubmitForm(prefix=str(assignment.id))
        context = {'assigned_problems': assigned_problems}
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
            assign_task = Assignment(person=User.objects.get(id=int(student)),
                                     problem=Problem.objects.get(id=int(problem)), date_deadline=date_deadline,
                                     assigned_by=request.user).save()
    for group_id in request.POST.getlist('group'):
        group = Group.objects.get(id=group_id)
        for student in group.user_set.all():
            for problem in request.POST.getlist('problem'):
                assign_task = Assignment(person=student, problem=Problem.objects.get(id=int(problem)),
                                         date_deadline=date_deadline, assigned_by=request.user).save()
    return redirect('index')


def submit(request):
    def clean(string):
        string = string.replace(" ", "")
        string = string.replace(",", ".")
        return string

    def autocheck_answer(student, author):
        for answer in author.split(';'):  # several correct answers could be separated by ;
            if clean(answer) == clean(student):
                return True
        return False

    assignment = Assignment.objects.get(id=request.POST["assignment_id"])
    student_short_answer = request.POST[request.POST["assignment_id"] + "-short_answer"]
    answer_autoverdict = autocheck_answer(student_short_answer, assignment.problem.short_answer)
    Submit(assignment=assignment, short_answer=request.POST[request.POST["assignment_id"] + "-short_answer"],
           solution=request.POST[request.POST["assignment_id"] + "-solution"],
           answer_autoverdict=answer_autoverdict).save()
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
    submit.assignment.status = 2  # assignment solution checked
    submit.save()
    submit.assignment.save()
    return redirect('index')


def test(request):
    # object = Source.objects.get(id=SOURCE_ROOT)
    object = Topic.objects.get(id=TOPIC_ROOT)
    object_list = tree2List(object)
    return render(request, 'problems/object_level.html', {'object_list': object_list})


def source_list(request):  # generate source_list of all children
    source_ids = list(map(int, request.POST.getlist('source')))
    for source_id in source_ids:
        for child in Source.objects.get(id=source_id).children.all():
            source_ids.append(child.id)
        if not Source.objects.get(id=source_id).children.all():
            pass
    return source_ids


class ProblemDetailView(DetailView):
    model = Problem


def tree2List(root, counter):
    # children should be referenced as children in model class
    try:
        result = {'object': root, 'children': [], 'count': counter[root.id]}
    except:
        result = {'object': root, 'children': [], 'count': -1}

    children = root.children.all()
    if children:
        for child in children:
            if not 'Задача ' in child.name:  # don't show sources like "Задача #16'
                result['children'].append(tree2List(child, counter))

    return result


def filter_problems(request):
    filter_topics = list(map(int, request.POST.getlist('topic'))) or [TOPIC_ROOT]
    filter_sources = list(map(int, request.POST.getlist('source'))) or [SOURCE_ROOT]
    problems = Problem.objects.all()
    probs, tests, cases = [], [], []
    for problem in problems:
        for source in problem.source_set.all():
            while source.id not in filter_sources and source.id != SOURCE_ROOT:
                source = source.parent
            if source.id in filter_sources:
                for topic in problem.topics.all():
                    while topic.id not in filter_topics and topic.id != TOPIC_ROOT:
                        topic = topic.parent
                    if topic.id in filter_topics:
                        if problem.problem_type == 0:
                            probs.append(problem)
                        elif problem.problem_type == 4:
                            cases.append(problem)
                        else:
                            tests.append(problem)
                        break
                break

    return (probs, tests, cases)

def bulk_create_users(request):
    # csv file format: usernamme;password;email;last_name;firstname;
    if request.method == 'POST':
        result = []
        students = Group.objects.get(name='students')
        text =  request.FILES['csvfile'].read().decode('utf=8').split()
        for line in text:
            try:
                username, password, email, last_name, first_name, *_ = line.split(';')
            except:
                username, password, email, last_name, first_name, *_ = line.split(';')
            user=User(
                username=username,
                email=email,
                password=make_password(password),
                last_name=last_name,
                first_name=first_name,
                is_active=True,
            )
            user.save()
            user.groups.add(students)
            user.save()

    return render(request, 'problems/bulk_users.html', {})

def bulk_create_sources(request):
    # csv file format: existing_source_name;new_source_name;new_subsource_nams;...;
    if request.method == 'POST':
        text =  request.FILES['csvfile'].read().decode('utf=8').split("\r\n")
        print(text)
        for line in text:
            if not line:
                break   # empty line in the end of file
            sources = line.split(';')
            parent_source = Source.objects.get(name=sources[0])
            print(type(parent_source))
            for source in sources[1:]:
                if not source:
                    break   # empty field in the end of line
                if Source.objects.filter(name=source, parent=parent_source).count() == 1:
                    parent_source = Source.objects.get(name=source, parent=parent_source)
                    print('***')
                    print(parent_source.children.all())
                else:
                    if parent_source.children.all():
                        order = int(list(parent_source.children.all())[-1].order) + 1
                    else:
                        order = 1
                    new_source = Source(name=source, parent=parent_source, order=order)
                    new_source.save()
                    parent_source=new_source
                    print(order)

    return render(request, 'problems/bulk_sources.html', {})

def count_problems_by_source():
    counter = dict()
    source = Source.objects.get(id=SOURCE_ROOT)
    count_problems_by_source_dfs(source, counter)
    return counter

def count_problems_by_topic():
    counter = dict()
    topic = Topic.objects.get(id=TOPIC_ROOT)
    count_problems_by_topic_dfs(topic, counter)
    return counter

def count_problems_by_source_dfs(source, counter):
    if source.problem:
        counter[source.id] = 1
    else:
        counter[source.id] = 0
        for child in source.children.all():
            counter[source.id] += count_problems_by_source_dfs(child, counter)

    return counter[source.id]

def count_problems_by_topic_dfs(topic, counter):
    if topic.leaf:
        counter[topic.id] = len(topic.problems.all())
    else:
        counter[topic.id] = 0
        for child in topic.children.all():
            counter[topic.id] += count_problems_by_topic_dfs(child, counter)

    return counter[topic.id]
