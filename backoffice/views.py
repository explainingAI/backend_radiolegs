import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
    writer.writerow(["IMG ID", "Trust", "Experiment", "Start", "End"])

    start_exp = None
    start = None
    for ans in answers:
        if start_exp != ans.start_time:
            start_exp = ans.start_time
            start = start_exp

        writer.writerow([ans.image.pk, ans.trust, experiment_id, start, ans.end_time])

        start = ans.end_time

    return response