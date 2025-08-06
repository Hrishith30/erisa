from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from claims.models import ClaimList, ClaimDetail
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Reload claims data from CSV files with overwrite or append options'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            choices=['overwrite', 'append'],
            default='overwrite',
            help='Mode: overwrite (delete existing) or append (keep existing)'
        )
        parser.add_argument(
            '--claim-list',
            type=str,
            help='Path to claim list CSV file'
        )
        parser.add_argument(
            '--claim-detail',
            type=str,
            help='Path to claim detail CSV file'
        )

    def handle(self, *args, **options):
        mode = options['mode']
        claim_list_path = options['claim_list'] or 'Data/claim_list_data.csv'
        claim_detail_path = options['claim_detail'] or 'Data/claim_detail_data.csv'

        self.stdout.write(f"Starting data reload in {mode} mode...")

        try:
            with transaction.atomic():
                if mode == 'overwrite':
                    self.stdout.write("Deleting existing data...")
                    ClaimList.objects.all().delete()
                    ClaimDetail.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS("Existing data deleted"))

                # Load claim list data
                if os.path.exists(claim_list_path):
                    self.stdout.write(f"Loading claim list data from {claim_list_path}...")
                    claim_list_df = pd.read_csv(claim_list_path, delimiter='|')
                    
                    claim_list_objects = []
                    for _, row in claim_list_df.iterrows():
                        claim_list_objects.append(ClaimList(
                            id=row['id'],
                            patient_name=row['patient_name'],
                            billed_amount=row['billed_amount'],
                            paid_amount=row['paid_amount'],
                            status=row['status'],
                            insurer_name=row['insurer_name'],
                            discharge_date=row['discharge_date']
                        ))
                    
                    ClaimList.objects.bulk_create(claim_list_objects, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Loaded {len(claim_list_objects)} claim list records"))
                else:
                    self.stdout.write(self.style.WARNING(f"Claim list file not found: {claim_list_path}"))

                # Load claim detail data
                if os.path.exists(claim_detail_path):
                    self.stdout.write(f"Loading claim detail data from {claim_detail_path}...")
                    claim_detail_df = pd.read_csv(claim_detail_path, delimiter='|')
                    
                    claim_detail_objects = []
                    for _, row in claim_detail_df.iterrows():
                        claim_detail_objects.append(ClaimDetail(
                            id=row['id'],
                            claim_id=row['claim_id'],
                            denial_reason=row['denial_reason'],
                            cpt_codes=row['cpt_codes']
                        ))
                    
                    ClaimDetail.objects.bulk_create(claim_detail_objects, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Loaded {len(claim_detail_objects)} claim detail records"))
                else:
                    self.stdout.write(self.style.WARNING(f"Claim detail file not found: {claim_detail_path}"))

                self.stdout.write(self.style.SUCCESS("Data reload completed successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during data reload: {str(e)}"))
            raise CommandError(f"Data reload failed: {str(e)}")
