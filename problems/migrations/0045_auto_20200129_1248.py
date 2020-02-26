# Generated by Django 3.0.2 on 2020-01-29 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0044_auto_20200129_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.IntegerField(choices=[(0, 'Решение не сдано'), (2, 'Проверено учителем'), (3, 'Проверено автоматически'), (1, 'Ожидает проверки')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='problem_type',
            field=models.IntegerField(choices=[(4, 'Качественная задача'), (1, 'Тест с ответом ДА/НЕТ'), (3, 'Тест с выбором нескольких ответов'), (2, 'Тест с выбором одного ответа'), (0, 'Задача')], default=0, verbose_name='Тип задачи'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='yesno_answer',
            field=models.IntegerField(blank=True, choices=[(0, '---'), (1, 'Да'), (2, 'Нет')], default=None, verbose_name='Ответ ДА/НЕТ'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='yesno_answer',
            field=models.IntegerField(choices=[(0, '---'), (1, 'Да'), (2, 'Нет')], default=0, verbose_name='Ответ ДА/НЕТ'),
        ),
    ]