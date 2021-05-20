from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField


class GroupTeacher(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='teacher')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_group')

    def __str__(self):
        return "{} ({})".format(self.group, self.teacher)



class Topic(models.Model):
    name = models.CharField('Название', max_length=200)
    parent = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='children', verbose_name='Предок', null=True, blank=True)
    order = models.IntegerField('Порядковый номер')
    leaf = models.BooleanField('Конечная вершина (можно привязывать задачи)', default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


YESNO_CHOICES = {
    (0, '---'),
    (1, 'Да'),
    (2, 'Нет'),
}


TYPE_CHOICES = {
    (0, 'Задача'),
    (1, 'Тест с ответом ДА/НЕТ'),
    (2, 'Тест с выбором одного ответа'),
    (3, 'Тест с выбором нескольких ответов'),
    (4, 'Качественная задача'),
}


class PaperObject(models.Model):
    name = models.CharField('Название', max_length=200, blank=True, null=True)
    task = RichTextUploadingField('Условие')
    # class Meta:
    #     abstract = True
    #     ordering = ["name"]



class Problem(PaperObject):
    # name = models.CharField('Название', max_length=200, blank=True, null=True)
    # task = RichTextUploadingField('Условие')
    problem_type = models.IntegerField('Тип задачи', choices=TYPE_CHOICES, blank=False, null=False, default=0)
    short_answer = models.CharField('Ответ (для автоматической проверки)', max_length=200, blank=True)
    yesno_answer = models.IntegerField('Ответ ДА/НЕТ', choices=YESNO_CHOICES, blank=False, default=0)

    # TODO long_answer =
    # TODO subproblem_answers

    solution = RichTextUploadingField('Решение', blank=True)

    # TODO author
    # TODO difficulty
    # TODO attributes: производная, парабола итп
    # TODO LOGS
    #   TODO pub_date = models.DateTimeField('date published')
    #   TODO edit_date = models.DateTimeField('date last editied')
    #   TODO pub_user =
    #   TODO edit_user =
    #   TODO pictures_quality : draft, final
    #   TODO text_quality: draft, final


    hint = RichTextUploadingField('Подсказка', blank=True)

    topics = models.ManyToManyField(Topic, related_name="problems", verbose_name='Темы')

    assignments = models.ManyToManyField(User, through='Assignment', through_fields=['problem', 'person'])

    def __str__(self):
        result = "#" + str(self.id)
        if self.source_set.all():
            result += ". " + ", ".join(map(str, self.source_set.all()))
        if self.name:
            result += ". " + self.name
        return result + ". " + self.task[:30] + "..."

    class Meta:
        ordering = ['id']


class Variant(models.Model):
    text = models.CharField('Вариант ответа', max_length=1000, blank=False)
    right = models.BooleanField('Верный ответ', blank=False, null=False, default=False)
    problem = models.ForeignKey(Problem, verbose_name="Задача", on_delete=models.CASCADE, blank=True, null=True, related_name='variants')
    order = models.IntegerField('Порядковый номер', blank=False, null=False, default=0)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return mark_safe(self.text)


class Source(models.Model):
    name = models.CharField('Название', max_length=200)
    parent = models.ForeignKey('Source', on_delete=models.CASCADE, verbose_name="Предок", related_name='children',
                               blank=True, null=True)
    order = models.IntegerField('Порядковый номер')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        try: # recursion could raise error
            if self.parent:
                return "{} - {}".format(self.parent, self.name)
            else:
                return self.name
        except:
            return self.name

    class Meta:
        ordering = ['id']


STATUS_CHOICES = {
    (0, 'Решение не сдано'),
    (1, 'Ожидает проверки'),
    (2, 'Проверено учителем'),
    (3, 'Проверено автоматически'),
}

class Assignment(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому задано')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='Задача')
    date_assigned = models.DateField('Когда задано', auto_now_add=True, blank=False)
    date_deadline = models.DateField('Сдать до', blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigner', verbose_name='Кем задано')
    status = models.IntegerField('Статус', choices = STATUS_CHOICES, null=False, blank=False, default=0)

    def __str__(self):
        return "{} -> {}. {} {}".format(self.problem, self.person.id, self.person.last_name, self.person.first_name)

    class Meta:
        ordering = ['status', 'date_deadline']

class TestSet(models.Model):
    name = models.CharField('Название', max_length=200)
    problems = models.ManyToManyField(Problem)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests_assigner', verbose_name='Кем задано')

    def __str__(self):
        return self.name



class Theory(PaperObject):
    # name = models.CharField('Название', max_length=200, blank=True, null=True)
    # task = RichTextUploadingField('Текст')
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Paper(models.Model):
    title = models.CharField('Название', max_length=200, blank=True, null=True)
    blocks = models.ManyToManyField(PaperObject)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='papers_assigner',
                                    verbose_name='Кем задано')
    def __str__(self):
        return self.title

class TaskOrder(models.Model):
    paper = models.ForeignKey(Paper, verbose_name="Последовательность", on_delete=models.CASCADE, blank=True, default=-1, related_name='task_order')
    number = models.CharField('номер PaperObject', max_length=1000, blank=False)
    order = models.IntegerField('номер объекта в листе', blank=False, null=False, default=-1)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return mark_safe(self.number)

class TestSetAssignment(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому задано')
    test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE, verbose_name='Тест', related_name="assignments")
    date_assigned = models.DateField('Когда задано', auto_now_add=True, blank=False)
    date_deadline = models.DateField('Сдать до', blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testset_assigner', verbose_name='Кем задано')
    status = models.IntegerField('Статус', choices=STATUS_CHOICES, null=False, blank=False, default=0)

    def __str__(self):
        return "{} -> {}. {} {}".format(self.test_set, self.person.id, self.person.last_name, self.person.first_name)

    class Meta:
        ordering = ['date_deadline']


class PaperAssignment(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кому задано')
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, verbose_name='Лист', related_name="paper_assignments")
    date_assigned = models.DateField('Когда задано', auto_now_add=True, blank=False)
    date_deadline = models.DateField('Сдать до', blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paper_assigner', verbose_name='Кем задано')
    status = models.IntegerField('Статус', choices=STATUS_CHOICES, null=False, blank=False, default=0)

    def __str__(self):
        return "{} -> {}. {} {}".format(self.paper, self.person.id, self.person.last_name, self.person.first_name)

    class Meta:
        ordering = ['date_deadline']




VERDICT_CHOICES = [
    (-1, 'Не проверено учителем'),
    (0, 'Неверное решение'),
    (1, 'Частично верное решение'),
    (2, 'Верное решение с недочетами'),
    (3, 'Верное решение'),
]

class Submit(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Назначенная задача', related_name='submits')
    short_answer = models.CharField('Ответ (для автоматической проверки)', max_length=200, blank=True)
    yesno_answer = models.IntegerField('Ответ ДА/НЕТ', choices=YESNO_CHOICES, blank=False, null=False, default=0)
    multiplechoice_answer = models.CharField('Выбор ответов', max_length=200, blank=True, null=True)
    solution = RichTextUploadingField('Решение', blank=True, null=True)
    submit_datetime = models.DateTimeField('Время и дата сдачи решения', auto_now_add=True, blank=False)
    answer_autoverdict = models.BooleanField('Результат автоматической проверки', blank=True, null=True)
    verdict = models.IntegerField('Результат проверки учителем', choices=VERDICT_CHOICES, blank=False, null=False, default=-1)
    teacher_comment = RichTextUploadingField('Комментарий учителя', blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.assignment, self.submit_datetime, self.get_verdict_display())

class TestSubmit(models.Model):
    assignment = models.ForeignKey(TestSetAssignment, on_delete=models.CASCADE, verbose_name='Назначенный тест', related_name='submits')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='Задача', related_name='test_submits')
    yesno_answer = models.IntegerField('Ответ ДА/НЕТ', choices=YESNO_CHOICES, blank=False, null=False, default=0)
    multiplechoice_answer = models.CharField('Выбор ответов', max_length=200, blank=True, null=True)
    submit_datetime = models.DateTimeField('Время и дата сдачи решения', auto_now_add=True, blank=False)
    answer_autoverdict = models.BooleanField('Результат автоматической проверки', blank=True, null=True)

    def __str__(self):
        return '{} {}: {}'.format(self.assignment, self.submit_datetime, self.problem)

