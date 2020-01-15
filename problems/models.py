from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Topic(models.Model):
    name = models.CharField('Название', max_length=200)
    parent = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='children', verbose_name='Предок', null=True, blank=True)
    order = models.IntegerField('Порядковый номер')
    leaf = models.BooleanField('Конечная вершина (можно привязывать задачи)', default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Problem(models.Model):
    name = models.CharField('Название', max_length=200, blank=True, null=True)
    task = RichTextUploadingField('Условие')
    short_answer = models.CharField('Ответ (для автоматической проверки)', max_length=200, blank=True)
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
    # TODO yes/no question
    # TODO ABCD answers (radiobuttons)
    # TODO checkboxes
    # TODO problem_type - стандартные, олимпиадные

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


class Source(models.Model):
    name = models.CharField('Название', max_length=200)
    parent = models.ForeignKey('Source', on_delete=models.CASCADE, verbose_name="Предок", related_name='children',
                               blank=True, null=True)
    order = models.IntegerField('Порядковый номер')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.parent:
            return "{} - {}".format(self.parent, self.name)
        else:
            return self.name

    class Meta:
        ordering = ['order']


STATUS_CHOICES = {
    (0, 'Решение не сдано'),
    (1, 'Решение не проверено'),
    (2, 'Решение проверено'),
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

VERDICT_CHOICES = [
    (-1, 'Решение не проверено'),
    (0, 'Неверное решение'),
    (1, 'Частично верное решение'),
    (2, 'Верное решение с недочетами'),
    (3, 'Верное решение'),
]

class Submit(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Назначенная задача', related_name='submits')
    short_answer = models.CharField('Ответ (для автоматической проверки)', max_length=200, blank=True)
    solution = RichTextUploadingField('Решение', blank=True)
    submit_datetime = models.DateTimeField('Время и дата сдачи решения', auto_now_add=True, blank=False)
    answer_autoverdict = models.BooleanField('Результат автоматической проверки ответа', blank=True, null=True)
    verdict = models.IntegerField('Результат проверки', choices=VERDICT_CHOICES, blank=False, null=False, default=-1)
    teacher_comment = RichTextUploadingField('Комментарий учителя', blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.assignment, self.submit_datetime, self.get_verdict_display())

