from django.contrib import admin
from .models import ClaimList, ClaimDetail, ClaimFlag, ClaimNote

@admin.register(ClaimList)
class ClaimListAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'status', 'insurer_name', 'discharge_date', 'billed_amount', 'paid_amount')
    list_filter = ('status', 'insurer_name', 'discharge_date')
    search_fields = ('id', 'patient_name', 'insurer_name')
    ordering = ('-discharge_date',)
    list_per_page = 50

@admin.register(ClaimDetail)
class ClaimDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim_id', 'denial_reason', 'cpt_codes')
    list_filter = ('denial_reason',)
    search_fields = ('id', 'claim_id', 'denial_reason', 'cpt_codes')
    ordering = ('-id',)
    list_per_page = 50

@admin.register(ClaimFlag)
class ClaimFlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim', 'user', 'flagged_at', 'reason', 'is_resolved')
    list_filter = ('is_resolved', 'flagged_at')
    search_fields = ('claim__id', 'user__username', 'reason')
    ordering = ('-flagged_at',)

@admin.register(ClaimNote)
class ClaimNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'claim', 'user', 'created_at', 'note')
    list_filter = ('created_at',)
    search_fields = ('claim__id', 'user__username', 'note')
    ordering = ('-created_at',)
