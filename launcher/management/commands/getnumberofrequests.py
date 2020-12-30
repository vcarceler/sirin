from django.core.management.base import BaseCommand, CommandError
from launcher.models import Request

class Command(BaseCommand):
    help = 'Get the number of pending requests for a label.'

    def add_arguments(self, parser):
        parser.add_argument('label', nargs=1, type=str, default='default', help='Indicates the label for the requests.')
    
    def handle(self, *args, **options):
        result = Request.objects.filter(processed=False,label=options['label'][0])
        self.stdout.write('{0}'.format(result.count()))