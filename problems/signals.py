from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Source
from economics.settings import SOURCE_ROOT


@receiver(pre_save, sender=Source)
def post_save_handler(sender, **kwargs):
    source = kwargs['instance']
    problem = source.problem
    while source.id != SOURCE_ROOT:
        source = source.parent
        source.problems.add(problem)
