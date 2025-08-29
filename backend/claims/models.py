from django.db import models
from django.contrib.auth.models import User

class ClaimList(models.Model):
    """Model for claim list data"""
    id = models.BigIntegerField(primary_key=True)
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    billed_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    insurer_name = models.CharField(max_length=255, blank=True, null=True)
    discharge_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'claim_list'
        verbose_name = 'Claim List'
        verbose_name_plural = 'Claim Lists'

    def __str__(self):
        return f"{self.id} - {self.patient_name}"

class ClaimDetail(models.Model):
    """Model for claim detail data"""
    id = models.IntegerField(primary_key=True)
    claim_id = models.BigIntegerField()
    denial_reason = models.CharField(max_length=500, blank=True, null=True)
    cpt_codes = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'claim_detail'
        verbose_name = 'Claim Detail'
        verbose_name_plural = 'Claim Details'

    def __str__(self):
        return f"{self.id} - Claim {self.claim_id}"

    @property
    def claim_list(self):
        """Get the related claim list record"""
        return ClaimList.objects.filter(id=self.claim_id).first()

class ClaimFlag(models.Model):
    """Model for flagging claims for review"""
    claim = models.ForeignKey(ClaimList, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flagged_at = models.DateTimeField()
    reason = models.CharField(max_length=500, blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_flags')

    class Meta:
        db_table = 'claim_flag'
        verbose_name = 'Claim Flag'
        verbose_name_plural = 'Claim Flags'

    def __str__(self):
        return f"Flag {self.id} - Claim {self.claim.id}"

class ClaimNote(models.Model):
    """Model for adding notes to claims"""
    claim = models.ForeignKey(ClaimList, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'claim_note'
        verbose_name = 'Claim Note'
        verbose_name_plural = 'Claim Notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Note {self.id} - Claim {self.claim.id}"
