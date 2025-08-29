from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
from claims.models import ClaimList, ClaimDetail
from decimal import Decimal
from datetime import datetime
from pathlib import Path
import csv
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load claims data from existing SQLite database into Django models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load claims data...'))
        
        try:
            # Load claim list data
            self.load_claim_list_data()
            
            # Load claim detail data
            self.load_claim_detail_data()
            
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded all claims data!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading claims data: {str(e)}')
            )

    def load_claim_list_data(self):
        """Load claim list data from CSV files in the Data folder"""
        self.stdout.write('Loading claim list data...')
        
        # Clear existing data
        ClaimList.objects.all().delete()
        
        data_folder = Path(settings.BASE_DIR.parent) / 'Data'
        csv_path = data_folder / 'claim_list_data.csv'
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'CSV not found: {csv_path}'))
            self.stdout.write(self.style.WARNING('Skipping claim list load'))
            return
        
        claim_list_objects = []
        with csv_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            rows = list(reader)
            self.stdout.write(f'Found {len(rows)} rows in {csv_path.name}')
            
            for i, row in enumerate(rows):
                try:
                    id_val = int(row.get('id') or 0)
                    patient_name = row.get('patient_name') or ''
                    status = row.get('status') or ''
                    insurer_name = row.get('insurer_name') or ''
                    
                    discharge_date_str = row.get('discharge_date')
                    discharge_date_obj = None
                    if discharge_date_str:
                        try:
                            discharge_date_obj = datetime.strptime(discharge_date_str, '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            discharge_date_obj = None
                    
                    billed_amount_str = row.get('billed_amount')
                    billed_amount_decimal = None
                    if billed_amount_str not in (None, ''):
                        try:
                            billed_amount_decimal = Decimal(billed_amount_str)
                        except Exception:
                            billed_amount_decimal = None
                    
                    paid_amount_str = row.get('paid_amount')
                    paid_amount_decimal = None
                    if paid_amount_str not in (None, ''):
                        try:
                            paid_amount_decimal = Decimal(paid_amount_str)
                        except Exception:
                            paid_amount_decimal = None
                    
                    claim_list_objects.append(ClaimList(
                        id=id_val,
                        patient_name=patient_name,
                        billed_amount=billed_amount_decimal,
                        paid_amount=paid_amount_decimal,
                        status=status,
                        insurer_name=insurer_name,
                        discharge_date=discharge_date_obj,
                    ))
                except Exception as e:
                    if i < 5:
                        self.stdout.write(self.style.WARNING(f'Skipping row {i+1} due to error: {e}'))
                    continue
        
        if claim_list_objects:
            ClaimList.objects.bulk_create(claim_list_objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Loaded {len(claim_list_objects)} claim list records'))
        else:
            self.stdout.write(self.style.WARNING('No claim list objects to create'))

    def load_claim_detail_data(self):
        """Load claim detail data from CSV files in the Data folder"""
        self.stdout.write('Loading claim detail data...')
        
        # Clear existing data
        ClaimDetail.objects.all().delete()
        
        data_folder = Path(settings.BASE_DIR.parent) / 'Data'
        csv_path = data_folder / 'claim_detail_data.csv'
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'CSV not found: {csv_path}'))
            self.stdout.write(self.style.WARNING('Skipping claim detail load'))
            return
        
        claim_detail_objects = []
        with csv_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            rows = list(reader)
            self.stdout.write(f'Found {len(rows)} rows in {csv_path.name}')
            
            for i, row in enumerate(rows):
                try:
                    id_val = int(row.get('id') or 0)
                    claim_id = int(row.get('claim_id') or 0)
                    denial_reason = row.get('denial_reason') or ''
                    cpt_codes = row.get('cpt_codes') or ''
                    
                    claim_detail_objects.append(ClaimDetail(
                        id=id_val,
                        claim_id=claim_id,
                        denial_reason=denial_reason,
                        cpt_codes=cpt_codes,
                    ))
                except Exception as e:
                    if i < 5:
                        self.stdout.write(self.style.WARNING(f'Skipping row {i+1} due to error: {e}'))
                    continue
        
        if claim_detail_objects:
            ClaimDetail.objects.bulk_create(claim_detail_objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Loaded {len(claim_detail_objects)} claim detail records'))
        else:
            self.stdout.write(self.style.WARNING('No claim detail objects to create'))
