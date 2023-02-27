from django.db import models
from django.conf import settings


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
