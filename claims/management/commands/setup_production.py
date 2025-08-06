from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Set up production environment with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up production environment...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )
        
        # Load initial data if it exists
        try:
            self.stdout.write('Loading initial claims data...')
            call_command('load_claims_data')
            self.stdout.write(
                self.style.SUCCESS('Initial data loaded successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not load initial data: {e}')
            )
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput')
        
        self.stdout.write(
            self.style.SUCCESS('Production setup completed successfully!')
        )
