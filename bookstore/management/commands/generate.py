from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Generating the fake data'

    def _generate(self, multiplier):
        pass

    def add_arguments(self, parser):
        parser.add_argument('multiplier', nargs='+', type=int)

    def handle(self, *args, **options):
        for multiplier in options['multiplier']:
            self._generate(multiplier)

            self.stdout.write(self.style.SUCCESS('Successfully generated'))
