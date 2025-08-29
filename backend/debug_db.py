import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'claims_interface.settings')
django.setup()

from django.db import connection
from claims.models import ClaimList, ClaimDetail

# Test direct database connection
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM claim_list")
claim_list_count = cursor.fetchone()[0]
print(f'Direct DB claim_list count: {claim_list_count}')

cursor.execute("SELECT COUNT(*) FROM claim_detail")
claim_detail_count = cursor.fetchone()[0]
print(f'Direct DB claim_detail count: {claim_detail_count}')

# Test Django models
django_claim_list_count = ClaimList.objects.count()
django_claim_detail_count = ClaimDetail.objects.count()
print(f'Django models claim_list count: {django_claim_list_count}')
print(f'Django models claim_detail count: {django_claim_detail_count}')

# Try to create a test record
try:
    test_claim = ClaimList(
        id=99999,
        patient_name='Test Patient',
        billed_amount=100.00,
        paid_amount=50.00,
        status='Test',
        insurer_name='Test Insurer',
        discharge_date='2022-01-01'
    )
    test_claim.save()
    print('Successfully created test record')
except Exception as e:
    print(f'Error creating test record: {e}')

# Check if the test record was created
test_count = ClaimList.objects.filter(id=99999).count()
print(f'Test record count: {test_count}')
