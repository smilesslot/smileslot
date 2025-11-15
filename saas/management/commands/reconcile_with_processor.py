"""
The reconcile_with_processor command is will check all payouts on the processor
have been accounted for in the local database.
"""

import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from ...utils import datetime_or_now, get_organization_model
from ...backends import ProcessorError


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Reconcile processor payouts with transactions in the local
 database"""

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
            dest='dry_run', default=False,
            help='Do not commit transactions')
        parser.add_argument('--after', action='store',
            dest='after', default=None,
           help='Only accounts for records created *after* a specific datetime')
        parser.add_argument('--at-time', action='store',
            dest='at_time', default=None,
            help='Specifies the time at which the command runs')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        created_at = options['after']
        if created_at:
            created_at = datetime_or_now(created_at)
        # XXX currently unused
        # end_period = datetime_or_now(options['at_time'])
        if dry_run:
            LOGGER.warning("dry_run: no changes will be committed.")
        self.run_reconcile(created_at=created_at, dry_run=dry_run)

    def run_reconcile(self, created_at=None, dry_run=False):
        for provider in get_organization_model().objects.filter(is_provider=True):
            self.stdout.write("reconcile payouts for %s ..." % str(provider))
            backend = provider.processor_backend
            if not created_at:
                created_at = provider.created_at
            try:
                with transaction.atomic():
                    backend.reconcile_transfers(provider, created_at,
                        dry_run=dry_run)
            except ProcessorError as err:
                self.stderr.write("error: %s" % str(err))
