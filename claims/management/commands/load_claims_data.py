from django.core.management.base import BaseCommand
from django.db import connection
from claims.models import ClaimList, ClaimDetail
from decimal import Decimal
from datetime import datetime
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
        """Load claim list data from the existing database"""
        self.stdout.write('Loading claim list data...')
        
        # Clear existing data
        ClaimList.objects.all().delete()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, patient_name, billed_amount, paid_amount, status, insurer_name, discharge_date FROM claim_list")
            rows = cursor.fetchall()
            
            self.stdout.write(f'Found {len(rows)} rows in claim_list table')
            
            # Create new records
            claim_list_objects = []
            for i, row in enumerate(rows):
                (id_val, patient_name, billed_amount, paid_amount, status, insurer_name, discharge_date) = row
                
                if i < 5:  # Only show first 5 for debugging
                    self.stdout.write(f'Processing row {i+1}: {id_val}, {patient_name}')
                
                # Convert date string to date object if it exists
                discharge_date_obj = None
                if discharge_date:
                    try:
                        discharge_date_obj = datetime.strptime(discharge_date, '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        discharge_date_obj = None
                
                # Convert amounts to Decimal
                billed_amount_decimal = None
                if billed_amount is not None:
                    try:
                        billed_amount_decimal = Decimal(str(billed_amount))
                    except (ValueError, TypeError):
                        billed_amount_decimal = None
                
                paid_amount_decimal = None
                if paid_amount is not None:
                    try:
                        paid_amount_decimal = Decimal(str(paid_amount))
                    except (ValueError, TypeError):
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
            
            # Bulk create all records
            if claim_list_objects:
                ClaimList.objects.bulk_create(claim_list_objects, ignore_conflicts=True)
                self.stdout.write(
                    self.style.SUCCESS(f'Loaded {len(claim_list_objects)} claim list records'))
            else:
                self.stdout.write(self.style.WARNING('No claim list objects to create'))

    def load_claim_detail_data(self):
        """Load claim detail data from the existing database"""
        self.stdout.write('Loading claim detail data...')
        
        # Clear existing data
        ClaimDetail.objects.all().delete()
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, claim_id, denial_reason, cpt_codes FROM claim_detail")
            rows = cursor.fetchall()
            
            self.stdout.write(f'Found {len(rows)} rows in claim_detail table')
            
            # Create new records
            claim_detail_objects = []
            for i, row in enumerate(rows):
                (id_val, claim_id, denial_reason, cpt_codes) = row
                
                if i < 5:  # Only show first 5 for debugging
                    self.stdout.write(f'Processing row {i+1}: {id_val}, {claim_id}')
                
                claim_detail_objects.append(ClaimDetail(
                    id=id_val,
                    claim_id=claim_id,
                    denial_reason=denial_reason,
                    cpt_codes=cpt_codes,
                ))
            
            # Bulk create all records
            if claim_detail_objects:
                ClaimDetail.objects.bulk_create(claim_detail_objects, ignore_conflicts=True)
                self.stdout.write(
                    self.style.SUCCESS(f'Loaded {len(claim_detail_objects)} claim detail records'))
            else:
                self.stdout.write(self.style.WARNING('No claim detail objects to create'))
