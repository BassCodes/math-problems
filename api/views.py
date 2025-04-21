from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from problems.models import Problem
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def individual_problem(request, pid):
    if request.method == "GET":
        try:
            problem_data = Problem.objects.get(pk=pid)
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={"error": "Not Found"})

        data_object = {"problem_text": problem_data.problem_text}

        return JsonResponse(data_object, safe=True)
