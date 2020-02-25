from datetime import datetime
import re

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.views.generic.detail import DetailView
from django.contrib.auth.hashers import make_password

from economics.settings import TOPIC_ROOT, SOURCE_ROOT


from .models import Assignment, Problem, Topic, Submit, Source, Variant, TestSet, TestSetAssignment, TestSubmit
from .forms import SubmitForm, CheckForm

# Create your views here.


def index(request):
    if request.user.groups.filter(name='teachers').exists():
        # Teacher index
        probs, tests, cases = filter_problems(request)
        students = User.objects.filter(groups__name='students')
        groups = Group.objects.all()
        topic = Topic.objects.get(id=TOPIC_ROOT)
        topic_list = tree2List(topic, count_problems_by_topic())
        source = Source.objects.get(id=SOURCE_ROOT)
        testsets = TestSet.objects.all()
        source_list = tree2List(source, count_problems_by_source())
        submits = Submit.objects.filter(assignment__assigned_by=request.user).filter(assignment__status=1)  # solution not checked
        context = {'problems': probs,
                   'tests': tests,
                   'cases': cases,
                   'students': students,
                   'topic_list': topic_list,
                   'source_list': source_list,
                   'submits': submits,
                   'groups': groups,
                   'testsets': testsets,
                   }
        return render(request, 'problems/sb/index_teacher.html', context)

    elif request.user.groups.filter(name='students').exists():
        # Student index
        assigned_problems = Assignment.objects.filter(person=request.user).order_by('status', 'date_deadline')
        problems = []
        for assignment in assigned_problems:
            problem = assignment.problem
            problem.assignment = assignment
            problem.assignment.form = SubmitForm(prefix=str(assignment.id), problem=assignment.problem)
            problems.append(problem)
        assigned_testsets = TestSetAssignment.objects.filter(person=request.user, status=0)
        solved_testsets = TestSetAssignment.objects.filter(person=request.user, status=3)

        context = {'assigned_problems': problems, 'assigned_testsets': assigned_testsets, 'solved_testsets': solved_testsets}
        return render(request, 'problems/sb/index_student.html', context)

    else:
        return render(request, 'problems/sb/login.html', {})


def assign(request):
    if request.POST['submit'] == 'Назначить задачи':
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

    elif request.POST['submit'] == 'Создать тест':
        # create TestSet
        test_set = TestSet(name=request.POST["name"])
        test_set.save()
        for problem in request.POST.getlist('problem'):
            test_set.problems.add(Problem.objects.get(id=int(problem)))

    elif request.POST['submit'] == 'Назначить тесты':
        if request.POST['date_deadline']:
            date_test_deadline = datetime.strptime(request.POST['date_deadline'], "%Y-%m-%d")
        else:
            date_test_deadline = None
        # create AssignTestSet
        for test_set_id in request.POST.getlist('testset'):
            test_set = TestSet.objects.get(id=int(test_set_id))
            for student in request.POST.getlist('student'):
                TestSetAssignment(person=User.objects.get(id=int(student)), test_set=test_set,
                              date_deadline=date_test_deadline,
                              assigned_by=request.user
                              ).save()

    return redirect('index')


def clean(string):
    string = string.replace(" ", "")
    string = string.replace(",", ".")
    return string


def autocheck_answer(student, author):
    for answer in author.split(';'):  # several correct answers could be separated by ;
        if clean(answer) == clean(student):
            return True
    return False


def check_yesno_answer(student, author):
    return int(student) == author


def check_single_choice(student, author):
    correct = author.get(right=True).id
    return int(student) == correct


def check_multiple_choice(student, author):
    correct = author.filter(right=True).values_list('id', flat=True)
    return set(map(int, student)) == set(correct)


def testset_submit(request):
    assignment = TestSetAssignment.objects.get(pk=int(request.POST["assigned_id"]))
    tests = assignment.test_set.problems.all()
    for test in tests:
        submit = TestSubmit(problem=test, assignment=assignment)
        id = str(test.id)
        if test.problem_type == 1:
            student_yesno_answer = submit.yesno_answer = request.POST[id + "-yesno_answer"]
            submit.answer_autoverdict = check_yesno_answer(student_yesno_answer, test.yesno_answer)
        elif test.problem_type == 2:
            student_single_answer = submit.multiplechoice_answer = request.POST[id + "-variants"]
            submit.answer_autoverdict = check_single_choice(student_single_answer, test.variants.all())
        elif test.problem_type == 3:
            student_multiple_answer = submit.multiplechoice_answer = request.POST.getlist(id + "-variants")
            submit.answer_autoverdict = check_multiple_choice(student_multiple_answer, test.variants)
        submit.save()
    assignment.status = 3
    assignment.save()
    return redirect('index')



def submit(request):
    id = request.POST["assignment_id"]
    assignment = Assignment.objects.get(id=id)

    submit = Submit(assignment=assignment)


    if assignment.problem.problem_type == 0:
        student_short_answer = submit.short_answer = request.POST[id + "-short_answer"]
        submit.solution = request.POST[id + "-solution"]
        submit.answer_autoverdict = autocheck_answer(student_short_answer, assignment.problem.short_answer)
        assignment.status = 1
    elif assignment.problem.problem_type == 1:
        student_yesno_answer = submit.yesno_answer = request.POST[id + "-yesno_answer"]
        submit.answer_autoverdict = check_yesno_answer(student_yesno_answer, assignment.problem.yesno_answer)
        assignment.status = 3
    elif assignment.problem.problem_type == 2:
        student_single_answer = submit.multiplechoice_answer = request.POST[id + "-variants"]
        submit.answer_autoverdict = check_single_choice(student_single_answer, assignment.problem.variants.all())
        assignment.status = 3
    elif assignment.problem.problem_type == 3:
        student_multiple_answer = submit.multiplechoice_answer=request.POST.getlist(id + "-variants")
        submit.answer_autoverdict = check_multiple_choice(student_multiple_answer, assignment.problem.variants)
        assignment.status = 3
    elif assignment.problem.problem_type == 4:
        submit.solution = request.POST[id + "-solution"]
        assignment.status = 1

    submit.save()
    assignment.save()

    return redirect("index")


def check_solution(request, submit_id):
    submit = Submit.objects.get(id=submit_id)
    problem = submit.assignment.problem
    problem.submit = submit
    if request.user == submit.assignment.assigned_by:
        form = CheckForm()
        context = {'form': form, 'submit': submit, 'problem': problem}
        return render(request, 'problems/check_solution.html', context)
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
        for line in text:
            if not line:
                break   # empty line in the end of file
            sources = line.split(';')
            parent_source = Source.objects.get(name=sources[0])
            for source in sources[1:]:
                if not source:
                    break   # empty field in the end of line
                if Source.objects.filter(name=source, parent=parent_source).count() == 1:
                    parent_source = Source.objects.get(name=source, parent=parent_source)

                else:
                    if parent_source.children.all():
                        order = int(list(parent_source.children.all())[-1].order) + 1
                    else:
                        order = 1
                    new_source = Source(name=source, parent=parent_source, order=order)
                    new_source.save()
                    parent_source=new_source

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


def submit_detail(request, pk):
    submit = Submit.objects.get(pk=pk)
    problem = submit.assignment.problem
    problem.submit = submit
    return render(request, 'problems/submit_detail.html', {'problem': problem})


def load_test(request):
    IN_TASK = 1
    IN_VARIANT = 2
    BEFORE = 3
    problem_number = 0
    state = BEFORE
    variant_text = None
    economics = Topic.objects.get(pk=TOPIC_ROOT)
    if request.POST:
        source_id = request.POST['source_id']
        test_text = request.POST['test_text']
        parent_source = Source.objects.get(id=source_id)
        problem_type = int(request.POST["problem_type"])
        if request.POST['topic_id']:
            topic_id = request.POST['topic_id']
            parent_topic = Topic.objects.get(id=topic_id)

        for line in test_text.split('\n'):
            line = line.lstrip()
            if state == BEFORE:
                print('BEFORE')
                yesno_answer = 0
                choice = None
                variant_counter = 0
                result = re.match(r'^\s*([+-12345абвгдАБВГД]*)\s*(\d+)\. (.*)$', line)
                if result:
                    answer = result.group(1)
                    if answer:
                        print(result.group(1))
                        if answer == '+':
                            yesno_answer = 1
                            print(1)
                        if answer == '-':
                            yesno_answer = 2
                            print(2)
                        if answer in '1аА':
                            choice = 1
                        if answer in '2бБ':
                            choice = 2
                        if answer in '3вВ':
                            choice = 3
                        if answer in '4гГ':
                            choice = 4
                        if answer in '5дД':
                            choice = 5
                    state = IN_TASK
                    problem_number = int(result.group(2)) or (problem_number + 1)
                    text = result.group(3)
            elif state == IN_TASK:
                print('IN_TASK type:', problem_type, line)
                if problem_type != 1 and (line.startswith("а)") or line.startswith("б)") or line.startswith("в)") or line.startswith("г)") or line.startswith("А)") or line.startswith("Б)") or line.startswith("В)") or line.startswith("Г)")  or line.startswith("+")):
                    print('Not type 1', problem_type)
                    problem = Problem(task=text, problem_type=3, yesno_answer=yesno_answer)
                    problem.save()
                    if request.POST['topic_id']:
                        problem.topics.add(topic_id)
                    else:
                        problem.topics.add(economics)
                    Source(name="Задача {}".format(problem_number), order=problem_number, parent = parent_source, problem=problem).save()
                    text = None
                    state = IN_VARIANT
                    right = line.startswith('+')
                    if line.startswith('+'):
                        variant_text = line[4:]
                        variant_order = (ord(line[1].lower()) - ord('a')) + 1
                    else:
                        variant_text = line[3:]
                        variant_order = (ord(line[0].lower()) - ord('a')) + 1
                elif problem_type == 1 and (line=="" or re.match(r'^\s*$', line) or re.match(r'^\s*([+-12345абвгдАБВГД]*)\s*(\d+)\. (.*)$', line)):
                    print('IN YES/NO - END')
                    problem = Problem(task=text, problem_type=1, yesno_answer=yesno_answer)
                    problem.save()
                    if request.POST['topic_id']:
                        problem.topics.add(topic_id)
                    else:
                        problem.topics.add(economics)
                    Source(name="Задача {}".format(problem_number), order=problem_number, parent=parent_source,
                           problem=problem).save()
                    text = None
                    state = BEFORE
                else:
                    print('append:', line, '$')
                    text = text + line
            elif problem_type != 1 and state == IN_VARIANT:
                print('IN VARIANT', line, "problem type:", problem_type, "$")
                result = re.match(r'^(\d+)\. (.*)$', line)
                if line.startswith("a)") or line.startswith("б)") or line.startswith("в)") or line.startswith(
                    "г)") or line.startswith("д)") or line.startswith("А)") or line.startswith("Б)") or line.startswith("В)") or line.startswith(
                    "Г)") or line.startswith("Д)") or line.startswith("+"):
                    variant_counter += 1
                    if choice:  # right answer before task number
                        if variant_counter == choice:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                        else:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
                    else:  # right answer before variant number
                        variant = Variant(text=variant_text, order=variant_order, problem=problem,
                                          right=line.startswith('+'))
                    variant.save()
                    right = line.startswith('+')
                    if right:
                        variant_text = line[4:]
                        variant_order = (ord(line[1].lower()) - ord('a')) + 1
                    else:
                        variant_text = line[3:]
                        variant_order = (ord(line[0].lower()) - ord('a')) + 1
                elif line=="":
                    variant_counter += 1
                    if choice: # right answer before task number
                        if variant_counter == choice:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                        else:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
                    else: # right answer before variant number
                        variant = Variant(text=variant_text, order=variant_order, problem=problem, right=line.startswith('+'))
                    variant.save()
                    state = BEFORE
                else:
                    variant_text = variant_text + line

        if problem_type == 1 and variant_text:
            variant_counter += 1
            if choice:  # right answer before task number
                if variant_counter == choice:
                    variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                else:
                    variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
            else:  # right answer before variant number
                variant = Variant(text=variant_text, order=variant_order, problem=problem, right=line.startswith('+'))
            variant.save()
        return render(request, 'problems/load_test.html', {})
    else:
        return render(request, 'problems/load_test.html', {})

def testset(request, pk):
    result = []
    assigned_testset = TestSetAssignment.objects.get(pk=pk)
    for problem in assigned_testset.test_set.problems.all():
        problem.form = SubmitForm(prefix=str(problem.id), problem=problem)
        result.append(problem)
    return render(request, 'problems/solve_testset.html', {'assigned_tests': result, 'assigned': assigned_testset})

def test_result(request, test_assignment_id):
    test_assignment = TestSetAssignment.objects.get(pk=test_assignment_id)
    result = []
    for problem in test_assignment.test_set.problems.all():
        problem.submit =TestSubmit.objects.get(problem=problem, assignment=test_assignment)
        result.append(problem)
    return render(request, 'problems/testset_result.html', {'tests': result})

def testset_all_results(request, testset_pk):
    testset = TestSet.objects.get(pk=testset_pk)
    results = []
    students = set(testset.assignments.values_list('person', flat=True))
    problem_list = testset.problems.all()

    for student_id in students:
        student = User.objects.get(pk=student_id)
        results.append(["{} {}".format(student.last_name, student.first_name)])
        score = 0
        for problem in problem_list:
            submits = TestSubmit.objects.filter(problem=problem, assignment__person=student)
            for submit in submits:
                if submit.answer_autoverdict is True:
                    results[-1].append(True)
                    score += 1
                    break
            else:
                results[-1].append(False)
        results[-1].append(score)
    return render(request, 'problems/testset_all_results.html', {'problems': problem_list, 'results':results})

def test(request):
    problem = Problem.objects.get(pk=23)
    #problem.submit = Submit.objects.get(pk=1)
    problem.assignment = Assignment.objects.get(pk=149)
    problem.assignment.form = SubmitForm(prefix=str(problem.assignment.id), problem=problem)

    return render(request, "problems/problem.html", {'problem': problem})
