from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Problem, Solution


@receiver(post_save, sender=Solution, dispatch_uid="link_solution_problem_history_save")
def add_solution_history_save_to_problem_history(sender, instance, **kwargs):
    solution = instance

    recent_problem_hist = solution.problem.history.first()

    recent_solution_hist = solution.history.first()
    recent_solution_hist.history_problem_ref = recent_problem_hist
    recent_solution_hist.save()
