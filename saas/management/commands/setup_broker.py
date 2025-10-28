from django.core.management.base import BaseCommand
from django.conf import settings
from saas.models import Organization
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates the initial broker organization for the application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            default='admin@smiles.co.ke',
            help='Email address for the broker organization'
        )
        parser.add_argument(
            '--name',
            default='SmileSlot Broker',
            help='Full name for the broker organization'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            broker_slug = getattr(settings, 'BROKER_CALLABLE', 'broker01')
            
            # Check if broker already exists
            broker = Organization.objects.filter(slug=broker_slug).first()
            
            if broker:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Broker organization already exists with slug: {broker_slug}'
                    )
                )
                return

            # Create new broker organization
            broker = Organization.objects.create(
                slug=broker_slug,
                full_name=options['name'],
                email=options['email'],
                is_active=True
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
            raise