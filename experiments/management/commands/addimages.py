import json

from django.core.management.base import BaseCommand, CommandError

from experiments import models


class Command(BaseCommand):
    help = 'Add images to database'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+')

    def handle(self, *args, **options):
        file_path = options['file'][0]
        with open(file_path) as f:
            data_file = json.load(f)

            for img_info in data_file["info"]:
                nom = img_info['nom']
                classe = img_info['classe']

                img = models.Image(name=nom, clase=classe)
                img.save()

                for exp_pk in img_info['experiments']:

                    try:
                        exp = models.Experiment.objects.get(pk=exp_pk)

                        ans = models.Answer(image=img, experiment=exp)
                        ans.save()
                    except models.Experiment.DoesNotExist:
                        raise CommandError(f"Experiment {exp_pk} does not exist")

            self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
