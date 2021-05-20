# Generated by Django 3.0.7 on 2021-05-17 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20210511_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.IntegerField(choices=[(2, 'Проверено учителем'), (3, 'Проверено автоматически'), (0, 'Решение не сдано'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='paperassignment',
            name='status',
            field=models.IntegerField(choices=[(2, 'Проверено учителем'), (3, 'Проверено автоматически'), (0, 'Решение не сдано'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='problem_type',
            field=models.IntegerField(choices=[(0, 'Задача'), (1, 'Тест с ответом ДА/НЕТ'), (2, 'Тест с выбором одного ответа'), (4, 'Качественная задача'), (3, 'Тест с выбором нескольких ответов')], default=0, verbose_name='Тип задачи'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='yesno_answer',
            field=models.IntegerField(choices=[(0, '---'), (1, 'Да'), (2, 'Нет')], default=0, verbose_name='Ответ ДА/НЕТ'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='yesno_answer',
            field=models.IntegerField(choices=[(0, '---'), (1, 'Да'), (2, 'Нет')], default=0, verbose_name='Ответ ДА/НЕТ'),
        ),
        migrations.AlterField(
            model_name='testsetassignment',
            name='status',
            field=models.IntegerField(choices=[(2, 'Проверено учителем'), (3, 'Проверено автоматически'), (0, 'Решение не сдано'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='testsubmit',
            name='yesno_answer',
            field=models.IntegerField(choices=[(0, '---'), (1, 'Да'), (2, 'Нет')], default=0, verbose_name='Ответ ДА/НЕТ'),
        ),
        migrations.CreateModel(
            name='TaskOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Порядковый номер')),
                ('paper_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_order', to='problems.Paper', verbose_name='Последовательность')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
            },
        ),
    ]
