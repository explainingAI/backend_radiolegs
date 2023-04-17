import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from experiments import models


# Create your views here.
def answer_2_csv(answer: models.Answer):
    nom_img = answer.image.name
    if "_" in nom_img:
        percent, nom = nom_img.split("_")
    else:
        percent, nom = 100, nom_img

    return [nom, answer.image.clase, percent, answer.trust, answer.experiment.pk]


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

        writer.writerow(answer_2_csv(answers) + [experiment_id, start, ans.end_time])

        start = ans.end_time

    return response


@login_required
def get_only_shared(request):
    experiments = models.Experiment.objects.all()

    aux = {}
    for exp in experiments:
        answers = exp.answer_set.all()
        for ans in answers:
            key = ans.image.name
            if key not in aux:
                aux[key] = []

            aux[key].append(ans)

    answers_shared = list(filter(lambda x: len(x) > 1, list(aux.values())))

    response = HttpResponse(
        content_type="text/csv",
        headers={f"Content-Disposition": f'attachment; filename="merged.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(
        ["IMG", "Class", "Percentatge"] + (["Trust", "Experiment"] * len(answers_shared[0])))

    for set_of_ans in answers_shared:
        aux = None

        for ans in set_of_ans:
            if aux is None:
                aux = answer_2_csv(ans)
            else:
                aux += [ans.trust, ans.experiment.pk]

        writer.writerow(aux)

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
