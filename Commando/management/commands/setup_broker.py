from django.core.management.base import BaseCommand
from django.conf import settings
from saas.models import Organization
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates the initial broker organization for the application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            default='admin@example.com',
            help='Email address for the broker organization'
        )
        parser.add_argument(
            '--name',
            default='Broker Organization',
            help='Full name for the broker organization'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            # Check if broker already exists
            broker = Organization.objects.filter(slug=settings.BROKER_CALLABLE).first()
            
            if broker:
                self.stdout.write(
                    self.style.WARNING(
                        f'Broker organization already exists with slug: {settings.BROKER_CALLABLE}'
                    )
                )
                return

            # Create new broker organization
            broker = Organization.objects.create(
                slug=settings.BROKER_CALLABLE,
                full_name=options['name'],
                email=options['email']
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created broker organization: {broker.full_name}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to create broker organization: {str(e)}'
                )
            )