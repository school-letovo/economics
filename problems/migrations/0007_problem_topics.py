# Generated by Django 3.0.2 on 2020-01-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20200110_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='topics',
            field=models.ManyToManyField(to='problems.Topic', verbose_name='Темы'),
        ),
    ]
