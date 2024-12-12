# Generated by Django 3.0.7 on 2021-05-22 14:42

from django.db import migrations, models
from economics.settings import SOURCE_ROOT


def assign_source_parents_to_problems(apps, schema_editor):
    print(end='\n (миграция может занять некоторое время) ')
    Problem, Source = (apps.get_model('problems', model) for model in ('Problem', 'Source'))
    problems = Problem.objects.all()
    problems_of_source_new = {}
    sources = {source['id']: source for source in Source.objects.values()}
    sources_by_problem = {}

    for source_id in sources:
        sources_by_problem.setdefault(sources[source_id]['problem_id'], set())
        sources_by_problem[sources[source_id]['problem_id']].add(source_id)

    for problem in problems:
        for source_id in sources_by_problem.get(problem.id, [SOURCE_ROOT]):
            source = sources[source_id]
            was_source_root = False
            while not was_source_root:
                if source['id'] == SOURCE_ROOT:
                    was_source_root = True
                problems_of_source_new.setdefault(source['id'], set())
                if problem.id not in problems_of_source_new[source['id']]:
                    problem.source_set.add(source['id'])
                    problems_of_source_new[source['id']].add(problem.id)
                if source['id'] != SOURCE_ROOT:
                    source = sources[source['parent_id']]



class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0057_auto_20200927_1253'),
    ]

    operations = [
        migrations.AddField(
            'Source', 'problems', models.ManyToManyField('Problem', blank=True, null=True, related_name='source_set')
        ),
        migrations.RunPython(assign_source_parents_to_problems, atomic=True),
        migrations.RemoveField('Source', 'problem')
    ]
