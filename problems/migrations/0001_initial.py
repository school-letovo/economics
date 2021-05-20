# Generated by Django 3.0.7 on 2021-05-10 08:34

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField(auto_now_add=True, verbose_name='Когда задано')),
                ('date_deadline', models.DateField(blank=True, null=True, verbose_name='Сдать до')),
                ('status', models.IntegerField(choices=[(0, 'Решение не сдано'), (3, 'Проверено автоматически'), (2, 'Проверено учителем'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigner', to=settings.AUTH_USER_MODEL, verbose_name='Кем задано')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кому задано')),
            ],
            options={
                'ordering': ['status', 'date_deadline'],
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers_assigner', to=settings.AUTH_USER_MODEL, verbose_name='Кем задано')),
            ],
        ),
        migrations.CreateModel(
            name='PaperObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название')),
                ('task', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Условие')),
            ],
        ),
        migrations.CreateModel(
            name='TestSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_assigner', to=settings.AUTH_USER_MODEL, verbose_name='Кем задано')),
            ],
        ),
        migrations.CreateModel(
            name='TestSetAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField(auto_now_add=True, verbose_name='Когда задано')),
                ('date_deadline', models.DateField(blank=True, null=True, verbose_name='Сдать до')),
                ('status', models.IntegerField(choices=[(0, 'Решение не сдано'), (3, 'Проверено автоматически'), (2, 'Проверено учителем'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testset_assigner', to=settings.AUTH_USER_MODEL, verbose_name='Кем задано')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кому задано')),
                ('test_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='problems.TestSet', verbose_name='Тест')),
            ],
            options={
                'ordering': ['date_deadline'],
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('paperobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='problems.PaperObject')),
                ('problem_type', models.IntegerField(choices=[(1, 'Тест с ответом ДА/НЕТ'), (0, 'Задача'), (3, 'Тест с выбором нескольких ответов'), (4, 'Качественная задача'), (2, 'Тест с выбором одного ответа')], default=0, verbose_name='Тип задачи')),
                ('short_answer', models.CharField(blank=True, max_length=200, verbose_name='Ответ (для автоматической проверки)')),
                ('yesno_answer', models.IntegerField(choices=[(2, 'Нет'), (1, 'Да'), (0, '---')], default=0, verbose_name='Ответ ДА/НЕТ')),
                ('solution', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Решение')),
                ('hint', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Подсказка')),
                ('assignments', models.ManyToManyField(through='problems.Assignment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('problems.paperobject',),
        ),
        migrations.CreateModel(
            name='Theory',
            fields=[
                ('paperobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='problems.PaperObject')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('problems.paperobject',),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('order', models.IntegerField(verbose_name='Порядковый номер')),
                ('leaf', models.BooleanField(default=False, verbose_name='Конечная вершина (можно привязывать задачи)')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='problems.Topic', verbose_name='Предок')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_answer', models.CharField(blank=True, max_length=200, verbose_name='Ответ (для автоматической проверки)')),
                ('yesno_answer', models.IntegerField(choices=[(2, 'Нет'), (1, 'Да'), (0, '---')], default=0, verbose_name='Ответ ДА/НЕТ')),
                ('multiplechoice_answer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Выбор ответов')),
                ('solution', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Решение')),
                ('submit_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата сдачи решения')),
                ('answer_autoverdict', models.BooleanField(blank=True, null=True, verbose_name='Результат автоматической проверки')),
                ('verdict', models.IntegerField(choices=[(-1, 'Не проверено учителем'), (0, 'Неверное решение'), (1, 'Частично верное решение'), (2, 'Верное решение с недочетами'), (3, 'Верное решение')], default=-1, verbose_name='Результат проверки учителем')),
                ('teacher_comment', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Комментарий учителя')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submits', to='problems.Assignment', verbose_name='Назначенная задача')),
            ],
        ),
        migrations.CreateModel(
            name='PaperAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_assigned', models.DateField(auto_now_add=True, verbose_name='Когда задано')),
                ('date_deadline', models.DateField(blank=True, null=True, verbose_name='Сдать до')),
                ('status', models.IntegerField(choices=[(0, 'Решение не сдано'), (3, 'Проверено автоматически'), (2, 'Проверено учителем'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_assigner', to=settings.AUTH_USER_MODEL, verbose_name='Кем задано')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paper_assignments', to='problems.Paper', verbose_name='Лист')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кому задано')),
            ],
            options={
                'ordering': ['date_deadline'],
            },
        ),
        migrations.AddField(
            model_name='paper',
            name='objects',
            field=models.ManyToManyField(to='problems.PaperObject'),
        ),
        migrations.CreateModel(
            name='GroupTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='auth.Group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_group', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, verbose_name='Вариант ответа')),
                ('right', models.BooleanField(default=False, verbose_name='Верный ответ')),
                ('order', models.IntegerField(default=0, verbose_name='Порядковый номер')),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='problems.Problem', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='TestSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yesno_answer', models.IntegerField(choices=[(2, 'Нет'), (1, 'Да'), (0, '---')], default=0, verbose_name='Ответ ДА/НЕТ')),
                ('multiplechoice_answer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Выбор ответов')),
                ('submit_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата сдачи решения')),
                ('answer_autoverdict', models.BooleanField(blank=True, null=True, verbose_name='Результат автоматической проверки')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submits', to='problems.TestSetAssignment', verbose_name='Назначенный тест')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_submits', to='problems.Problem', verbose_name='Задача')),
            ],
        ),
        migrations.AddField(
            model_name='testset',
            name='problems',
            field=models.ManyToManyField(to='problems.Problem'),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('order', models.IntegerField(verbose_name='Порядковый номер')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='problems.Source', verbose_name='Предок')),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='topics',
            field=models.ManyToManyField(related_name='problems', to='problems.Topic', verbose_name='Темы'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem', verbose_name='Задача'),
        ),
    ]
