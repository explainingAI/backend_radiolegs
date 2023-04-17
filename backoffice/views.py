import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from experiments import models


# Create your views here.

@login_required
def get_results(request, experiment_id):
    exp = models.Experiment.objects.get(pk=experiment_id)
    answers = exp.answer_set.all()

    response = HttpResponse(
        content_type="text/csv",
        headers={f"Content-Disposition": f'attachment; filename="exp_{experiment_id}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["IMG", "Class", "Percentatge", "Trust", "Experiment", "Start", "End"])

    start_exp = None
    start = None
    for ans in answers:
        if start_exp != ans.start_time:
            start_exp = ans.start_time
            start = start_exp

        nom_img = ans.image.name
        percent, nom = nom_img.split("_")

        writer.writerow([nom, ans.image.clase, percent, ans.trust, experiment_id, start, ans.end_time])

        start = ans.end_time

    return response


@login_required
def main(request):
    experiments = models.Experiment.objects.all()

    context = []
    for exp in experiments:
        total = len(exp.answer_set.all())
        answered = len(exp.answer_set.all().filter(~Q(trust=None)))

        context.append({"percent": round((total - answered) / total, 4) * 100, "exp": exp})

    return render(request, 'main.html', {"experiments": context})
