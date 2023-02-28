from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100)

    TIPUS = {
        "cov": "Patològic",
        "ncov": "No patològic"
    }

    clase = models.CharField(
        max_length=4,
        choices=TIPUS.items(),
        default=TIPUS['cov'],
        null=True,
    )

    @property
    def path_img(self):
        return f"{settings.IMG_URL}{self.name}.png"

    def __str__(self):
        return str(self.name)


class Experiment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.TimeField(auto_now=True)


class Answer(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    trust = models.BooleanField(default=None, null=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['image', 'experiment']]
