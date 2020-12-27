from django.core.management.base import BaseCommand, CommandError
from launcher.models import Request

class Command(BaseCommand):
    help = 'Get a list of hosts with not processed requests and marks requests as processed.'

    def add_arguments(self, parser):
        #parser.add_argument('get_ansible_limit', nargs='+', type=int)
        a=1

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Ansible limit: options: "%s"' % options ))