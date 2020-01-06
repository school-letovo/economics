from django.db import models

# Create your models here.

class Problem(models.Model):
    name = models.CharField('Название', max_length=200)
    task = models.TextField('Условие')
    short_answer = models.CharField('Ответ (для автоматической проверки)', max_length=200)
    # TODO long_answer =
    # TODO subproblem_answers

    solution = models.TextField('Решение')

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

    hint = models.TextField('Подсказка')

    def __str__(self):
        return "{}. {}".format(self.name, self.task[:30])


