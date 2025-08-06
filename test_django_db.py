import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claims_interface.settings')
django.setup()

from django.db import connection
from claims.models import ClaimList, ClaimDetail

# Test raw SQL query
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM claim_list")
raw_count = cursor.fetchone()[0]
print(f'Raw SQL count: {raw_count}')

# Test Django ORM
orm_count = ClaimList.objects.count()
print(f'Django ORM count: {orm_count}')

# Try to get a sample record
if raw_count > 0:
    cursor.execute("SELECT * FROM claim_list LIMIT 1")
    raw_record = cursor.fetchone()
    print(f'Raw SQL record: {raw_record}')

# Try to get a sample record via Django ORM
if orm_count > 0:
    django_record = ClaimList.objects.first()
    print(f'Django ORM record: {django_record}')
else:
    print('No records found via Django ORM')

# Check if we can create a record
try:
    test_claim = ClaimList(
        id=99998,
        patient_name='Test Patient 2',
        billed_amount=200.00,
        paid_amount=100.00,
        status='Test',
        insurer_name='Test Insurer',
        discharge_date='2022-01-01'
    )
    test_claim.save()
    print('Successfully created another test record')
except Exception as e:
    print(f'Error creating test record: {e}')

# Check the count again
final_count = ClaimList.objects.count()
print(f'Final count: {final_count}')
