from datetime import datetime
import re

from django.db.models import Count
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.views.generic.detail import DetailView
from django.contrib.auth.hashers import make_password

from economics.settings import TOPIC_ROOT, SOURCE_ROOT


from .models import Assignment, Problem, Topic, Submit, Source, Variant, TestSet, TestSetAssignment, TestSubmit, GroupTeacher
from .forms import SubmitForm, CheckForm

# Create your views here.


def index(request):
    if request.user.groups.filter(name='teachers').exists():
        # Teacher index
        # probs, tests, cases = filter_problems(request)
        if request.user.groups.filter(name='supervisor').exists():
            students = User.objects.filter(groups__name='students').order_by('last_name')
            groups = Group.objects.all()
            testsets = TestSet.objects.all()
        else:
            group_ids = GroupTeacher.objects.filter(teacher=request.user).values_list('group__id', flat=True)
            students = User.objects.filter(groups__in=group_ids).order_by('last_name')
            groups = Group.objects.filter(id__in=group_ids)
            testsets = TestSet.objects.filter(assigned_by=request.user)

        topic = Topic.objects.get(id=TOPIC_ROOT)
        topic_list = tree2List(topic, count_problems_by_topic())
        checked_topics = list(map(int, request.POST.getlist('topic'))) or [TOPIC_ROOT]
        checked_sources = list(map(int, request.POST.getlist('source'))) or [SOURCE_ROOT]
        source = Source.objects.get(id=SOURCE_ROOT)
        source_list = tree2List(source, count_problems_by_source())
        submits = Submit.objects.filter(assignment__assigned_by=request.user).filter(assignment__status=1)  # solution not checked
        context = {#'problems': probs,
                   #'tests': tests,
                   #'cases': cases,
                   'students': students,
                   'topic_list': topic_list,
                   'source_list': source_list,
                   'submits': submits,
                   'groups': groups,
                   'testsets': testsets,
                   'checked_topics': checked_topics,
                   'checked_sources': checked_sources,
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

def assign_problems(request):
    if request.POST['date_deadline']:
        date_deadline = datetime.strptime(request.POST['date_deadline'], "%Y-%m-%d")
    else:
        date_deadline = None
    for student in request.POST['student'].split(','):
        for problem in request.POST['problem'].split(','):
            assign_task = Assignment(person=User.objects.get(id=int(student)),
                                     problem=Problem.objects.get(id=int(problem)), date_deadline=date_deadline,
                                     assigned_by=request.user).save()
    for group_id in request.POST.getlist('group'):
        group = Group.objects.get(id=group_id)
        for student in group.user_set.all():
            for problem in request.POST.getlist('problem'):
                assign_task = Assignment(person=student, problem=Problem.objects.get(id=int(problem)),
                                         date_deadline=date_deadline, assigned_by=request.user).save()


def create_test(request):
    # create TestSet
    test_set = TestSet(name=request.POST["name"], assigned_by_id=request.user.id)
    test_set.save()
    for problem in request.POST['problem'].split(','):
        test_set.problems.add(Problem.objects.get(id=int(problem)))

def delete_test(request):
    # delete TestSet
    for test_set_id in request.POST.getlist('testset'):
        test_set = TestSet.objects.get(id=int(test_set_id))
        test_set.delete()

def assign_test(request):
    if request.POST['date_test_deadline']:
        date_test_deadline = datetime.strptime(request.POST['date_test_deadline'], "%Y-%m-%d")
    else:
        date_test_deadline = None
    # create AssignTestSet
    for test_set_id in request.POST.getlist('testset'):
        test_set = TestSet.objects.get(id=int(test_set_id))
        for student in request.POST.getlist('student'):
            try:
                TestSetAssignment.objects.get(person=User.objects.get(id=int(student)), test_set=test_set)
            except:  # тест еще не назначен
                TestSetAssignment(person=User.objects.get(id=int(student)), test_set=test_set,
                                  date_deadline=date_test_deadline,
                                  assigned_by=request.user
                                  ).save()
        for group_id in request.POST.getlist('group'):
            group = Group.objects.get(id=group_id)
            for student in group.user_set.all():
                assign_task = TestSetAssignment(person=student, test_set=test_set,
                                                date_deadline=date_test_deadline, assigned_by=request.user).save()


def assign(request):
    if request.POST['submit'] == 'Назначить задачи':
        assign_problems(request)
    elif request.POST['submit'] == 'Создать тест':
        create_test(request)
    elif request.POST['submit'] == 'Назначить тесты':
        assign_test(request)
    elif request.POST['submit'] == 'Удалить тесты':
        delete_test(request)

    return redirect('index')

def add_students(request):
    for student in request.POST.getlist('student'):
        for group_id in request.POST.getlist('group'):
            user = User.objects.get(id=int(student))
            user_group = Group.objects.get(id=group_id)
            user.groups.add(user_group)
            user.save()


    return redirect('index')

def add_students_to_groups(request):
    group_ids = GroupTeacher.objects.filter(teacher=request.user).values_list('group__id', flat=True)
    students = User.objects.annotate(numofgroups = Count('groups')).filter(numofgroups__lte = 1).order_by('last_name')
    groups = Group.objects.filter(id__in=group_ids)
    context = {'students': students, 'groups': groups,}
    if request.POST:
        return render(request, 'problems/add_students_to_groups.html', context)
    else:
        return render(request, 'problems/add_students_to_groups.html', context)


def clean(string):
    string = string.replace(" ", "")
    string = string.replace(",", ".")
    return string


def autocheck_answer(student, author):
    for answer in author.split(';'):  # several correct answers could be separated by ;
        if (clean(answer) ==
                clean(student)):
            return True
    return False


def check_yesno_answer(student, author):
    return int(student) == author


def check_single_choice(student, author):
    try:
        correct = author.get(right=True).id
    except: # в базе забыли внести правильный ответ или внесли несколько - трактуем в пользу ученика
        return True
    if '[' in student:
        test = student
        student = student[2:-2]

    if student == '':
        return False
    try:
        return int(student) == correct
    except:
        return False

def rejudge_test(request):
    if request.user.is_superuser:
        test_id = int(request.POST['test_id'])
        submits = TestSubmit.objects.filter(problem=test_id)
        for submit in submits:
            print(submit)
            if submit.problem.problem_type == 1:
                student_yesno_answer = submit.yesno_answer
                submit.answer_autoverdict = check_yesno_answer(student_yesno_answer, submit.problem.yesno_answer)
            elif submit.problem.problem_type == 2:
                student_single_answer = submit.multiplechoice_answer
                submit.answer_autoverdict = check_single_choice(student_single_answer, submit.problem.variants.all())
            elif submit.problem.problem_type == 3:
                student_multiple_answer = submit.multiplechoice_answer
                submit.answer_autoverdict = check_multiple_choice(student_multiple_answer, submit.problem.variants)
            elif submit.problem.problem_type == 5:
                student_open_answer = submit.short_answer
                submit.answer_autoverdict = autocheck_answer(student_open_answer, submit.problem.short_answer)
            submit.save()

    return redirect('index')

def check_multiple_choice(student, author):
    correct = author.filter(right=True).values_list('id', flat=True)
    return set(map(int, student)) == set(correct)

# @transaction.atomic - TODO потестить
def testset_submit(request):
    assignment = TestSetAssignment.objects.get(pk=int(request.POST["assigned_id"]))
    if assignment.status == 0: # исключаем возможность сдать второй раз, но это не очень надежно - нужны транзакции по-хорошему
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
            elif test.problem_type == 5:
                student_open_answer = submit.short_answer = request.POST.getlist(id + "-short_answer")
                submit.answer_autoverdict = autocheck_answer(student_open_answer[0], test.short_answer)

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



def filter_problems(request, problem_type=None):
    filter_topics = set(map(int, request.POST.getlist('topic'))) or {TOPIC_ROOT}
    filter_sources = set(map(int, request.POST.getlist('source'))) or {SOURCE_ROOT}
    if problem_type is None:
        problems = Problem.objects.filter(source_set__in=filter_sources)
    else:
        problems = Problem.objects.filter(problem_type__in=problem_type,
                                          source_set__in=filter_sources)
    probs, tests, cases = [], [], []
    for problem in problems:
        if problem_type is None:
            if problem.problem_type == 0:
                probs.append(problem)
            elif problem.problem_type == 4:
                cases.append(problem)
            else:
                tests.append(problem)
        elif problem_type == [0]:
            probs.append(problem)
        elif problem_type == [4]:
            cases.append(problem)
        else:
            tests.append(problem)

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


def count_problems_by_topic():
    return {topic.id: topic.problems.count for topic in Topic.objects.all()}


def count_problems_by_source():
    return {source.id: source.problems.count for source in Source.objects.all()}


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

    letters = ['a', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    numb_let = numbers + letters

    symb_bracket = [symb + ')' for symb in numb_let]
    upper_bracket = [letter.upper() + ')' for letter in letters]
    symb_dot = [symb + '.' for symb in numb_let]
    two_symb_filter = symb_bracket + upper_bracket + symb_dot

    if request.POST:
        source_id = int(request.POST['source_id'])
        test_text = request.POST['test_text']
        parent_source = Source.objects.get(id=source_id)
        problem_type = int(request.POST["problem_type"])
        if request.POST['topic_id']:
            topic_id = int(request.POST['topic_id'])
            parent_topic = Topic.objects.get(id=topic_id)

        for line in test_text.split('\n'):
            line = line.lstrip()
            if state == BEFORE:
                print('BEFORE')
                yesno_answer = 2
                choice = None
                variant_counter = 0
                variant_order = 0
                result = re.match(r'^\s*([\+\-aабвгдежзиAАБВГДЕЖЗИ]*)\s*(\d+)\.\s*(\(.+?\)+)?(.*)$', line)
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
                        if answer in '1aAаА':
                            choice = 1
                        if answer in '2бБ':
                            choice = 2
                        if answer in '3вВ':
                            choice = 3
                        if answer in '4гГ':
                            choice = 4
                        if answer in '5дД':
                            choice = 5
                        if answer in '6eE':
                            choice = 6
                        if answer in '7жЖ':
                            choice = 7
                        if answer in '8зЗ':
                            choice = 8
                        if answer in '9иИ':
                            choice = 9
                    state = IN_TASK
                    problem_number = (problem_number + 1)           ### int(result.group(2)) or
                    text = result.group(4)
                    print(result.group(3))
            elif state == IN_TASK:
                print('IN_TASK type:', problem_type, line)

                if problem_type != 1 and problem_type != 5 and (line.startswith("+") or (line[:2] in two_symb_filter)):
                    print('Not type 1, 5', problem_type)
                    problem = Problem(task=text, problem_type=problem_type)
                    problem.save()
                    if request.POST['topic_id']:
                        problem.topics.add(topic_id)
                    else:
                        problem.topics.add(economics)
                    text = None
                    state = IN_VARIANT
                    right = line.startswith('+')
                    if line.startswith('+'):
                        variant_text = line[4:]
                    else:
                        variant_text = line[3:]
                    oldline = line
                elif problem_type == 1 and (line=="" or re.match(r'^\s*$', line) or re.match(r'^\s*([+-aабвгдежзиAАБВГДЕЖЗИ]*)\s*(\d+)\.\s(.*)$', line)):
                    print('IN YES/NO - END')
                    problem = Problem(task=text, problem_type=1, yesno_answer=yesno_answer)
                    problem.save()
                    if request.POST['topic_id']:
                        problem.topics.add(topic_id)
                    else:
                        problem.topics.add(economics)
                    text = None
                    state = BEFORE
                elif problem_type == 1:
                    print('append:', line, '$')
                    text = text + line
                    oldline = line
                elif problem_type == 5:
                    result = re.match(r'^\s*\[(.+)\]\s*$', line)
                    if result:
                        open_answer = result.group(1)
                        print("open answer", open_answer)
                        problem = Problem(task=text, problem_type=5, short_answer=open_answer)
                        problem.save()
                        if request.POST['topic_id']:
                            problem.topics.add(topic_id)
                        else:
                            problem.topics.add(economics)
                        text = None
                        state = BEFORE
                    else:
                        print('append:', line, '$')
                        text = text + line
                        oldline = line
            elif problem_type != 1 and problem_type != 5 and state == IN_VARIANT:
                print('IN VARIANT', line, "problem type:", problem_type, "$")
                result = re.match(r'^(\d+)\. (.*)$', line)
                if problem_type != 1 and problem_type != 5 and (line.startswith("+") or (line[:2] in two_symb_filter)):
                    variant_counter += 1
                    variant_order += 1
                    if choice:  # right answer before task number
                        if variant_counter == choice:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                        else:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
                    else:  # right answer before variant number
                        print('variant order:', variant_order, oldline)
                        variant = Variant(text=variant_text, order=variant_order, problem=problem,
                                          right=oldline.startswith('+'))
                    variant.save()
                    right = line.startswith('+')
                    if right:
                        variant_text = line[4:]
                    else:
                        variant_text = line[3:]
                    oldline = line
                elif line == "":
                    variant_counter += 1
                    variant_order += 1
                    if choice: # right answer before task number
                        if variant_counter == choice:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                        else:
                            variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
                    else: # right answer before variant number
                        variant = Variant(text=variant_text, order=variant_order, problem=problem, right=oldline.startswith('+'))
                    variant.save()
                    state = BEFORE
                else:
                    variant_text = variant_text + line

        if problem_type == 1 and variant_text:
            variant_counter += 1
            variant_order += 1
            if choice:  # right answer before task number
                if variant_counter == choice:
                    variant = Variant(text=variant_text, order=variant_order, problem=problem, right=True)
                else:
                    variant = Variant(text=variant_text, order=variant_order, problem=problem, right=False)
            else:  # right answer before variant number
                variant = Variant(text=variant_text, order=variant_order, problem=problem, right=line.startswith('+'))
            variant.save()
        source = Source(name="Задача {}".format(problem_number), order=problem_number, parent=parent_source)
        source.problems.add(problem)
        source.save()
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
    if test_assignment.person != request.user:
        return redirect('index')
    result = []
    tests_ok = 0
    for problem in test_assignment.test_set.problems.all():
        problem.submit =TestSubmit.objects.get(problem=problem, assignment=test_assignment)
        if problem.submit.answer_autoverdict:
            tests_ok += 1
        result.append(problem)
    return render(request, 'problems/testset_result.html', {'tests': result, 'tests_ok': tests_ok, 'test_problems': test_assignment.test_set.problems})


def testset_all_results(request, testset_pk):
    testset = TestSet.objects.get(pk=testset_pk)
    results = []
    problem_list = testset.problems.all()
    n_problems = len(problem_list)
    problem_index = {problem.id: i + 2 for i, problem in enumerate(problem_list)}
    students = {assignment.person: assignment.submits.values('answer_autoverdict', 'problem')
                for assignment in testset.assignments.all().prefetch_related('submits', 'person')}
    for student in students:
        # Use no-break space in student name to avoid line breaking
        student_vals = {'name': student.last_name + ' ' + student.first_name, 'id': student.id}
        cur = [student_vals] + [0] + [None] * n_problems
        for submission in students[student]:
            if not cur[problem_index[submission['problem']]]:
                if submission['answer_autoverdict']:
                    cur[1] += 1
                    cur[problem_index[submission['problem']]] = submission['answer_autoverdict']
                else:
                    cur[problem_index[submission['problem']]] = submission['answer_autoverdict']
        results.append(cur)
    results.sort(key=lambda x: (-int(x[1]), x[0]['name']))
    return render(request, 'problems/testset_all_results.html', {'problems': problem_list,
                                                                 'results': results, 'testset_pk': testset_pk})


def test(request):
    problem = Problem.objects.get(pk=223)
    #problem.submit = Submit.objects.get(pk=1)
    #problem.assignment = Assignment.objects.get(pk=149)
    #problem.assignment.form = SubmitForm(prefix=str(problem.assignment.id), problem=problem)


def ajax_problems(request, start, amount, problem_type):
    if request.user.groups.filter(name='teachers').exists():
        # Teacher index
        if problem_type == 'prob':
            probs, tests, cases = filter_problems(request, [0])
            data = probs[(start-1) * amount:start * amount]
            length = len(probs)
        elif problem_type == 'test':
            probs, tests, cases = filter_problems(request, [1, 2, 3])
            data = tests[(start-1) * amount:start * amount]
            length = len(tests)
        else: # problem_type == 'case'
            probs, tests, cases = filter_problems(request, [4])
            data = cases[(start-1) * amount:start * amount]
            length = len(cases)
        result = {'length':length, 'html':render_to_string('problems/problem_list.html', {'problems':data, 'request':request})}
        return JsonResponse(result)


def failed_tests(request, student_id, testset_pk):
    testset = TestSet.objects.get(pk=testset_pk)
    student = User.objects.get(pk=student_id)
    problem_list = testset.problems.all()
    answer = []
    for problem in problem_list:
        negative_result = TestSubmit.objects.filter(assignment__person=student, problem=problem, answer_autoverdict=False).count()
        positive_result = TestSubmit.objects.filter(assignment__person=student, problem=problem, answer_autoverdict=True).count()
        if positive_result == 0 and negative_result > 0:
            answer.append(problem)
    return render(request, "problems/testset_result.html", {'tests': answer, 'student':student})

def create_user(request):
    if request.POST:
        # Create user and save to the database
        user = User.objects.create_user(request.POST['login'], request.POST['email'], request.POST['password'])

        # Update fields and then save again
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        group = Group.objects.get(name='studentsajax')
        group.user_set.add(user)

        return redirect('index')
    else:
        return render(request, "problems/sb/register.html", {})

def student_page(request, pk):
    student = User.objects.get(pk=pk)
    testsets = TestSetAssignment.objects.filter(person=student)

    return render(request, "problems/student_page.html", {'student': student, 'testsets': testsets})

def rejudge_page(request):
    if request.user.groups.filter(name='teachers').exists():
        return render(request, "problems/rejudge.html")
