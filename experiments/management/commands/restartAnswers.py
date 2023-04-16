from django.core.management.base import BaseCommand, CommandError

from experiments import models


class Command(BaseCommand):
    help = 'Restart all answers of the database'
    def handle(self, *args, **options):
        models.Answer.objects.update(trust=None)
        self.stdout.write(self.style.SUCCESS('Successfully restarted answers poll'))
