from django.core.management.base import BaseCommand, CommandError
from launcher.models import Request

class Command(BaseCommand):
    help = 'Get a list of pending requests.'

    # def add_arguments(self, parser):
    #     parser.add_argument('get_ansible_limit', nargs='+', type=int)
        

    def handle(self, *args, **options):
        self.stdout.write('{0:<8s} {1:<32s} {2:<32s} {3:<32s}'.format('ID', 'LABEL', 'ADDRESS', 'DATETIME'))

        for r in Request.objects.filter(processed=False):
            self.stdout.write('{0:<8d} {1:<32s} {2:<32s} {3:<32s}'.format(r.pk, r.label, r.address, str(r.datetime)))