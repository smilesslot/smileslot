import sys

from django.core.management.base import BaseCommand

from ...models import get_broker


class Command(BaseCommand):
    help = """Delete the (customer) account associated with an organization
from the payment processor service."""
    args = 'regex'

    def add_arguments(self, parser):
        parser.add_argument('-n', action='store_true', dest='no_execute',
            default=False, help='Print but do not execute')

    def handle(self, *args, **options):
        pat = r'.*'
        if args:
            pat = args[0]
        processor_backend = get_broker().processor_backend
        for cust in processor_backend.list_customers(pat):
            sys.stdout.write('%s %s\n' % (str(cust.id), str(cust.description)))
            if not options['no_execute']:
                cust.delete()
