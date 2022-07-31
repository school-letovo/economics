from django.db.models.signals import m2m_changed, pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Source, Topic, Problem
from economics.settings import SOURCE_ROOT, TOPIC_ROOT


@receiver(m2m_changed, sender=Problem.source_set.through)
def m2m_source_changed(sender, instance, pk_set, action=None, **kwargs):
    if isinstance(instance, Problem):
        problem = instance
        sources = pk_set
        if action == 'post_add':
            for source_id in sources:
                if source_id != SOURCE_ROOT:
                    Source.objects.get(pk=source_id).parent.problems.add(problem)
        elif action == 'pre_remove':
            for source_id in sources:
                if source_id != SOURCE_ROOT:
                    Source.objects.get(pk=source_id).parent.problems.remove(problem)
    else:
        source = instance
        problems = pk_set
        if source.id == SOURCE_ROOT:
            return
        if action == 'post_add':
            for problem_id in problems:
                source.parent.problems.add(problem_id)
        elif action == 'pre_remove':
            for problem_id in problems:
                source.parent.problems.remove(problem_id)


@receiver(m2m_changed, sender=Problem.topics.through)
def m2m_topic_changed(sender, instance, pk_set, action=None, **kwargs):
    if isinstance(instance, Problem):
        problem = instance
        topics = pk_set
        if action == 'pre_add':
            for topic_id in topics:
                if topic_id != TOPIC_ROOT:
                    Topic.objects.get(pk=topic_id).parent.problems.add(problem)
        elif action == 'pre_delete':
            for topic_id in topics:
                if topic_id != TOPIC_ROOT:
                    Topic.objects.get(pk=topic_id).parent.problems.remove(problem)
    else:
        topic = instance
        if topic.id == TOPIC_ROOT:
            return
        problems = pk_set
        if action == 'pre_add':
            for problem_id in problems:
                topic.parent.problems.add(problem_id)
        elif action == 'pre_delete':
            for problem_id in problems:
                topic.parent.problems.remove(problem_id)


@receiver(pre_delete, sender=Source)
@receiver(pre_delete, sender=Topic)
def source_topic_deleted(sender, instance, **kwargs):
    for problem_id in instance.problems.values_list('id', flat=True):
        instance.problems.remove(problem_id)


@receiver(pre_save, sender=Source)
@receiver(pre_save, sender=Topic)
def source_topic_parent_changed_presave(sender, instance, **kwargs):
    new_instance = instance
    if new_instance.id == TOPIC_ROOT and sender is Topic or new_instance.id == SOURCE_ROOT and sender is Source:
        return
    try:
        old_instance = sender.objects.get(pk=new_instance.pk)
    except (sender.DoesNotExist, ValueError):
        # do not remove problems from "old" parents
        pass
    else:
        if old_instance.parent_id == new_instance.parent_id:
            return
        for problem_id in new_instance.problems.values_list('id', flat=True):
            old_instance.parent.problems.remove(problem_id)


@receiver(post_save, sender=Source)
@receiver(post_save, sender=Topic)
def source_topic_parent_changed_postsave(sender, instance, **kwargs):
    new_instance = instance
    if new_instance.id == TOPIC_ROOT and sender is Topic or new_instance.id == SOURCE_ROOT and sender is Source:
        return
    for problem_id in new_instance.problems.values_list('id', flat=True):
        new_instance.parent.problems.add(problem_id)
