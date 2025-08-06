from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from claims.models import ClaimList, ClaimDetail
import csv
import os
from decimal import Decimal

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
                    
                    claim_list_objects = []
                    with open(claim_list_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter='|')
                        for row in reader:
                            # Convert empty strings to None for optional fields
                            billed_amount = Decimal(row['billed_amount']) if row['billed_amount'] else None
                            paid_amount = Decimal(row['paid_amount']) if row['paid_amount'] else None
                            
                            claim_list_objects.append(ClaimList(
                                id=int(row['id']),
                                patient_name=row['patient_name'] or None,
                                billed_amount=billed_amount,
                                paid_amount=paid_amount,
                                status=row['status'] or None,
                                insurer_name=row['insurer_name'] or None,
                                discharge_date=row['discharge_date'] if row['discharge_date'] else None
                            ))
                    
                    ClaimList.objects.bulk_create(claim_list_objects, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Loaded {len(claim_list_objects)} claim list records"))
                else:
                    self.stdout.write(self.style.WARNING(f"Claim list file not found: {claim_list_path}"))

                # Load claim detail data
                if os.path.exists(claim_detail_path):
                    self.stdout.write(f"Loading claim detail data from {claim_detail_path}...")
                    
                    claim_detail_objects = []
                    with open(claim_detail_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter='|')
                        for row in reader:
                            claim_detail_objects.append(ClaimDetail(
                                id=int(row['id']),
                                claim_id=int(row['claim_id']),
                                denial_reason=row['denial_reason'] or None,
                                cpt_codes=row['cpt_codes'] or None
                            ))
                    
                    ClaimDetail.objects.bulk_create(claim_detail_objects, ignore_conflicts=True)
                    self.stdout.write(self.style.SUCCESS(f"Loaded {len(claim_detail_objects)} claim detail records"))
                else:
                    self.stdout.write(self.style.WARNING(f"Claim detail file not found: {claim_detail_path}"))

                self.stdout.write(self.style.SUCCESS("Data reload completed successfully"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during data reload: {str(e)}"))
            raise CommandError(f"Data reload failed: {str(e)}")
