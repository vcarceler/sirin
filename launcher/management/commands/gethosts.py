from django.core.management.base import BaseCommand, CommandError
from launcher.models import Request

class Command(BaseCommand):
    help = 'Get a list of hosts with not processed requests and then marks requests as processed.'

    #def add_arguments(self, parser):
        #parser.add_argument('get_ansible_limit', nargs='+', type=int)
    
    def handle(self, *args, **options):
        for r in Request.objects.filter(processed=False):
            self.stdout.write('{0},'.format(r.address), ending='')
            r.processed=True
            r.save()