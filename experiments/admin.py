from django.contrib import admin
from .models import Image, Experiment, Answer

admin.site.register([Image, Experiment, Answer])
# Register your models here.
