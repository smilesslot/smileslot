
"""
Command to obliterate all traces of an Organization,
including Transaction history.
"""

from django.core.management.base import BaseCommand

from saas.utils import get_organization_model


class Command(BaseCommand):

    help = "Obliterate all traces of an Organization."

    def handle(self, *args, **options):
        #pylint: disable=too-many-locals
        organizations = get_organization_model().objects.filter(slug__in=args)
        organizations.delete()
