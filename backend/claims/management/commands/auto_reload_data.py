from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from claims.data_monitor import data_monitor
from claims.management.commands.load_claims_data import Command as LoadDataCommand
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically monitor CSV files and reload data when changes are detected'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Check interval in seconds (default: 30)'
        )
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuously (default: False)'
        )
    
    def handle(self, *args, **options):
        interval = options['interval']
        continuous = options['continuous']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting CSV file monitoring with {interval}s interval...'
            )
        )
        
        # Initialize the data monitor
        data_monitor.check_for_changes()
        
        if continuous:
            self.stdout.write('Running in continuous mode. Press Ctrl+C to stop.')
            try:
                while True:
                    self.check_and_reload()
                    time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write('\nStopping monitoring...')
        else:
            # Run once
            self.check_and_reload()
    
    def check_and_reload(self):
        """Check for changes and reload data if needed"""
        try:
            changes, current_hashes = data_monitor.check_for_changes()
            
            if changes:
                self.stdout.write(
                    self.style.WARNING(
                        f'Changes detected in {len(changes)} file(s):'
                    )
                )
                for change in changes:
                    self.stdout.write(f'  - {change}')
                
                # Reload data
                self.stdout.write('Reloading data...')
                self.reload_data()
                
                # Update cache timestamp
                cache.set('last_data_reload', timezone.now().isoformat(), timeout=3600)
                
                self.stdout.write(
                    self.style.SUCCESS('Data reload completed successfully!')
                )
            else:
                self.stdout.write('No changes detected.')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during monitoring: {e}')
            )
            logger.error(f'Error during data monitoring: {e}')
    
    def reload_data(self):
        """Reload all claims data"""
        try:
            # Use the existing load_claims_data command
            load_command = LoadDataCommand()
            load_command.handle()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reloading data: {e}')
            )
            logger.error(f'Error reloading data: {e}')
            raise
