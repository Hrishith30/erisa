from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.contrib.auth import login
from .models import ClaimList, ClaimDetail, ClaimFlag, ClaimNote
from .forms import UserSignUpForm
from .data_monitor import data_monitor
import json
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    """Main dashboard view with summary statistics"""
    # Get summary statistics (exclude test insurers)
    total_claims = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).count()
    total_billed = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).aggregate(total=Sum('billed_amount'))['total'] or 0
    total_paid = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).aggregate(total=Sum('paid_amount'))['total'] or 0
    
    # Calculate average claim amount
    average_claim = total_billed / total_claims if total_claims > 0 else 0
    
    # Flagged claims statistics
    total_flagged = ClaimFlag.objects.filter(is_resolved=False).count()
    resolved_flags = ClaimFlag.objects.filter(is_resolved=True).count()
    
    # Calculate average underpayment (difference between billed and paid)
    underpayment_data = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).filter(
        billed_amount__gt=0,
        paid_amount__lt=models.F('billed_amount')
    ).aggregate(
        avg_underpayment=Sum(models.F('billed_amount') - models.F('paid_amount')) / Count('id')
    )
    avg_underpayment = underpayment_data['avg_underpayment'] or 0
    
    # Claims by status (exclude test insurers)
    claims_by_status = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Claims by insurer (exclude test insurers)
    claims_by_insurer = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values('insurer_name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent claims (exclude test insurers)
    recent_claims = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).order_by('-discharge_date')[:10]
    
    context = {
        'total_claims': total_claims,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'average_claim': average_claim,
        'total_flagged': total_flagged,
        'resolved_flags': resolved_flags,
        'avg_underpayment': avg_underpayment,
        'claims_by_status': claims_by_status,
        'claims_by_insurer': claims_by_insurer,
        'recent_claims': recent_claims,
    }
    return render(request, 'claims/dashboard.html', context)

@login_required
def claim_list(request):
    """View for listing all claims with search and filtering"""
    claims = ClaimList.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        claims = claims.filter(
            Q(id__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(insurer_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        claims = claims.filter(status=status_filter)
    
    # Filter by insurer
    policy_filter = request.GET.get('policy', '')
    if policy_filter:
        claims = claims.filter(insurer_name=policy_filter)
    

    
    # Get unique values for filters (exclude test insurers)
    statuses = ClaimList.objects.values_list('status', flat=True).distinct()
    policies = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values_list('insurer_name', flat=True).distinct()
    
    # Pagination - add ordering to prevent inconsistent results
    claims = claims.order_by('id')  # Order by ID for consistent pagination
    paginator = Paginator(claims, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'policy_filter': policy_filter,
        'statuses': statuses,
        'policies': policies,
    }
    return render(request, 'claims/claim_list.html', context)

@login_required
def claim_detail(request, claim_id):
    """View for displaying detailed information about a specific claim"""
    claim = get_object_or_404(ClaimList, id=claim_id)
    claim_details = ClaimDetail.objects.filter(claim_id=claim_id)
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        import csv
        from django.http import HttpResponse
        
        try:
            # Build a safe filename using claim id and patient name
            patient_name = (claim.patient_name or 'patient').strip()
            safe_patient = ''.join(ch.lower() if ch.isalnum() else '-' for ch in patient_name)
            safe_patient = '-'.join(filter(None, safe_patient.split('-')))  # collapse repeats
            filename = f"{claim_id}-{safe_patient}.csv"
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Access-Control-Allow-Origin'] = '*'
            
            writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)
            # Header
            writer.writerow([
                'Claim ID',
                'Patient Name',
                'Insurer',
                'Status',
                'Discharge Date',
                'Billed Amount',
                'Paid Amount',
                'Detail ID',
                'CPT Codes',
                'Denial Reason',
            ])
            
            # Write one row per claim detail; include claim meta on each row
            details_qs = ClaimDetail.objects.filter(claim_id=claim_id).order_by('id')
            if details_qs.exists():
                for detail in details_qs:
                    # Normalize CPT codes: handle comma-separated or list-like strings
                    raw_codes = detail.cpt_codes or ''
                    if raw_codes:
                        parts = [p.strip().strip("[]'\"") for p in raw_codes.split(',')]
                        parts = [p for p in parts if p]
                        cpt_normalized = '; '.join(parts) if parts else '-'
                    else:
                        cpt_normalized = '-'
                    writer.writerow([
                        claim.id,
                        claim.patient_name or '-',
                        claim.insurer_name or '-',
                        claim.status or '-',
                        claim.discharge_date.strftime('%m/%d/%Y') if claim.discharge_date else '-',
                        f"{float(claim.billed_amount or 0):.2f}",
                        f"{float(claim.paid_amount or 0):.2f}",
                        detail.id,
                        cpt_normalized,
                        detail.denial_reason or '-',
                    ])
            else:
                # Write a single row with claim info if no details exist
                writer.writerow([
                    claim.id,
                    claim.patient_name or '-',
                    claim.insurer_name or '-',
                    claim.status or '-',
                    claim.discharge_date.strftime('%m/%d/%Y') if claim.discharge_date else '-',
                    f"{float(claim.billed_amount or 0):.2f}",
                    f"{float(claim.paid_amount or 0):.2f}",
                    '-',
                    '-',
                    '-',
                ])
            
            return response
        except Exception as e:
            # Return error response if CSV generation fails
            error_response = HttpResponse(f"Error generating CSV: {str(e)}", content_type='text/plain')
            error_response.status_code = 500
            return error_response
    
    # Calculate totals
    total_billed = claim.billed_amount or 0
    total_paid = claim.paid_amount or 0
    total_allowed = total_paid  # Since we don't have allowed amount in our model
    
    # Get flags and notes
    flags = claim.flags.all().order_by('-flagged_at')
    notes = claim.notes.all().order_by('-created_at')
    
    context = {
        'claim': claim,
        'claim_details': claim_details,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'total_allowed': total_allowed,
        'flags': flags,
        'notes': notes,
    }
    return render(request, 'claims/claim_detail.html', context)

@login_required
def claim_detail_htmx(request, claim_id):
    """HTMX view for claim detail without full page reload"""
    claim = get_object_or_404(ClaimList, id=claim_id)
    claim_details = ClaimDetail.objects.filter(claim_id=claim_id)
    
    # Calculate totals
    total_billed = claim.billed_amount or 0
    total_paid = claim.paid_amount or 0
    total_allowed = total_paid
    
    # Get flags and notes
    flags = claim.flags.all().order_by('-flagged_at')
    notes = claim.notes.all().order_by('-created_at')
    
    context = {
        'claim': claim,
        'claim_details': claim_details,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'total_allowed': total_allowed,
        'flags': flags,
        'notes': notes,
    }
    return render(request, 'claims/claim_detail_partial.html', context)

@login_required
def claim_details_list(request):
    """View for listing all claim details with search and filtering"""
    details = ClaimDetail.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        details = details.filter(
            Q(claim_id__icontains=search_query) |
            Q(denial_reason__icontains=search_query) |
            Q(cpt_codes__icontains=search_query)
        )
    
    # Filter by denial reason
    denial_filter = request.GET.get('denial_reason', '')
    if denial_filter:
        if denial_filter == 'No Denial':
            # Filter for records with no denial reason (None or empty)
            details = details.filter(denial_reason__isnull=True) | details.filter(denial_reason='')
        else:
            details = details.filter(denial_reason=denial_filter)
    
    # Get unique values for filters - exclude None values
    denial_reasons = ClaimDetail.objects.exclude(
        denial_reason__isnull=True
    ).exclude(
        denial_reason=''
    ).values_list('denial_reason', flat=True).distinct()
    
    # Pagination - add ordering to prevent inconsistent results
    details = details.order_by('id')  # Order by ID for consistent pagination
    
    paginator = Paginator(details, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'denial_filter': denial_filter,
        'denial_reasons': denial_reasons,
    }
    return render(request, 'claims/claim_details_list.html', context)

@login_required
def analytics(request):
    """Analytics view with charts and statistics"""

    
    # Get total claims count (exclude test insurers)
    total_claims = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).count()
    
    # Calculate total billed amount (exclude test insurers)
    total_billed = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).aggregate(total=Sum('billed_amount'))['total'] or 0
    
    # Claims by month (exclude test insurers) - using date function instead of strftime
    claims_by_month = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).extra(
        select={'month': "date(discharge_date, 'start of month')"}
    ).values('month').annotate(
        count=Count('id'),
        total_billed=Sum('billed_amount'),
        total_paid=Sum('paid_amount')
    ).order_by('month')
    
    # Claims by insurer (exclude test insurers)
    insurer_data = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values('insurer_name').annotate(
        count=Count('id'),
        total_billed=Sum('billed_amount'),
        total_paid=Sum('paid_amount')
    ).order_by('-total_paid')[:10]
    
    # Calculate averages for display
    for month in claims_by_month:
        month['average'] = month['total_billed'] / month['count'] if month['count'] > 0 else 0
    
    for insurer in insurer_data:
        insurer['average'] = insurer['total_paid'] / insurer['count'] if insurer['count'] > 0 else 0
    
    # Get first insurer for summary cards
    first_insurer = insurer_data[0] if insurer_data else None
    
    context = {
        'total_claims': total_claims,
        'total_billed': total_billed,
        'claims_by_month': list(claims_by_month),
        'insurer_data': list(insurer_data),
        'first_insurer': first_insurer,
    }
    return render(request, 'claims/analytics.html', context)

@login_required
def api_claims_data(request):
    """API endpoint for claims data (for charts)"""
    claims_data = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values('status').annotate(
        count=Count('id')
    )
    return JsonResponse({'data': list(claims_data)})

@login_required
def api_data_status(request):
    """API endpoint for data status and monitoring"""
    try:
        data_status = data_monitor.get_data_status()
        
        # Add database record counts
        data_status.update({
            'total_claims': ClaimList.objects.count(),
            'total_claim_details': ClaimDetail.objects.count(),
            'last_check': timezone.now().isoformat(),
        })
        
        return JsonResponse(data_status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_check_changes(request):
    """API endpoint to check for CSV changes"""
    try:
        changes, current_hashes = data_monitor.check_for_changes()
        
        response_data = {
            'changes_detected': len(changes) > 0,
            'changed_files': changes,
            'total_files': len(current_hashes),
            'last_check': timezone.now().isoformat(),
        }
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_force_reload(request):
    """API endpoint to force data reload"""
    try:
        from .management.commands.load_claims_data import Command as LoadDataCommand
        
        # Force reload data
        load_command = LoadDataCommand()
        load_command.handle()
        
        # Update cache timestamp
        from django.core.cache import cache
        cache.set('last_data_reload', timezone.now().isoformat(), timeout=3600)
        
        return JsonResponse({
            'success': True,
            'message': 'Data reload completed successfully',
            'reloaded_at': timezone.now().isoformat(),
            'total_claims': ClaimList.objects.count(),
            'total_claim_details': ClaimDetail.objects.count(),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def claim_list_htmx(request):
    """HTMX view for live search results"""
    claims = ClaimList.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        claims = claims.filter(
            Q(id__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(insurer_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        claims = claims.filter(status=status_filter)
    
    # Filter by insurer
    policy_filter = request.GET.get('policy', '')
    if policy_filter:
        claims = claims.filter(insurer_name=policy_filter)
    
    # Get unique values for filters (exclude test insurers)
    statuses = ClaimList.objects.values_list('status', flat=True).distinct()
    policies = ClaimList.objects.exclude(
        insurer_name__icontains='test'
    ).values_list('insurer_name', flat=True).distinct()
    
    # Pagination - add ordering to prevent inconsistent results
    claims = claims.order_by('id')  # Order by ID for consistent pagination
    paginator = Paginator(claims, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'policy_filter': policy_filter,
        'statuses': statuses,
        'policies': policies,
    }
    return render(request, 'claims/claim_list_partial.html', context)

@login_required
def flagged_claims(request):
    """List of flagged claims with pagination and basic filtering"""
    flags = ClaimFlag.objects.select_related('claim', 'user')

    status_filter = request.GET.get('status', '')
    if status_filter == 'open':
        flags = flags.filter(is_resolved=False)
    elif status_filter == 'resolved':
        flags = flags.filter(is_resolved=True)

    user_filter = request.GET.get('user', '')
    if user_filter:
        flags = flags.filter(user__username=user_filter)

    search_query = request.GET.get('search', '')
    if search_query:
        flags = flags.filter(
            Q(claim__id__icontains=search_query) |
            Q(claim__patient_name__icontains=search_query) |
            Q(reason__icontains=search_query)
        )

    flags = flags.order_by('-flagged_at')
    paginator = Paginator(flags, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'users': User.objects.values_list('username', flat=True).order_by('username'),
    }
    return render(request, 'claims/flagged_claims.html', context)

@login_required
def notes_list(request):
    """List of notes across claims with pagination and search"""
    notes = ClaimNote.objects.select_related('claim', 'user')

    search_query = request.GET.get('search', '')
    if search_query:
        notes = notes.filter(
            Q(claim__id__icontains=search_query) |
            Q(claim__patient_name__icontains=search_query) |
            Q(note__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    user_filter = request.GET.get('user', '')
    if user_filter:
        notes = notes.filter(user__username=user_filter)

    notes = notes.order_by('-created_at')
    paginator = Paginator(notes, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_filter': user_filter,
        'users': User.objects.values_list('username', flat=True).order_by('username'),
    }
    return render(request, 'claims/notes_list.html', context)


@login_required
def claim_details_list_htmx(request):
    """HTMX view for claim details live search results"""
    claim_details = ClaimDetail.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        claim_details = claim_details.filter(
            Q(id__icontains=search_query) |
            Q(claim_id__icontains=search_query)
        )
    
    # Filter by denial reason
    denial_filter = request.GET.get('denial_reason', '')
    if denial_filter:
        claim_details = claim_details.filter(denial_reason=denial_filter)
    
    # Get unique values for filters
    denial_reasons = ClaimDetail.objects.values_list('denial_reason', flat=True).distinct()
    
    # Pagination
    claim_details = claim_details.order_by('id')
    paginator = Paginator(claim_details, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'denial_filter': denial_filter,
        'denial_reasons': denial_reasons,
    }
    return render(request, 'claims/claim_details_list_partial.html', context)

@login_required
def flag_claim(request, claim_id):
    """Flag a claim for review"""
    if request.method == 'POST':
        claim = get_object_or_404(ClaimList, id=claim_id)
        reason = request.POST.get('reason', '')
        
        # Create new flag with explicit timestamp
        flag = ClaimFlag.objects.create(
            claim=claim,
            user=request.user,
            reason=reason,
            flagged_at=timezone.now()
        )
        
        if request.headers.get('HX-Request'):
            # Return the updated claim detail partial for HTMX
            claim = get_object_or_404(ClaimList, id=claim_id)
            claim_details = ClaimDetail.objects.filter(claim_id=claim_id)
            
            # Calculate totals
            total_billed = claim.billed_amount or 0
            total_paid = claim.paid_amount or 0
            total_allowed = total_paid
            
            # Get flags and notes
            flags = claim.flags.all().order_by('-flagged_at')
            notes = claim.notes.all().order_by('-created_at')
            
            context = {
                'claim': claim,
                'claim_details': claim_details,
                'total_billed': total_billed,
                'total_paid': total_paid,
                'total_allowed': total_allowed,
                'flags': flags,
                'notes': notes,
            }
            return render(request, 'claims/claim_detail_partial.html', context)
        return redirect('claims:claim_detail', claim_id=claim_id)
    
    return redirect('claims:claim_detail', claim_id=claim_id)

@login_required
def add_note(request, claim_id):
    """Add a note to a claim"""
    if request.method == 'POST':
        claim = get_object_or_404(ClaimList, id=claim_id)
        note_text = request.POST.get('note', '').strip()
        
        if note_text:
            note = ClaimNote.objects.create(
                claim=claim,
                user=request.user,
                note=note_text,
                created_at=timezone.now()
            )
        else:
            messages.error(request, 'Note cannot be empty.')
        
        if request.headers.get('HX-Request'):
            # Return the updated claim detail partial for HTMX
            claim = get_object_or_404(ClaimList, id=claim_id)
            claim_details = ClaimDetail.objects.filter(claim_id=claim_id)
            
            # Calculate totals
            total_billed = claim.billed_amount or 0
            total_paid = claim.paid_amount or 0
            total_allowed = total_paid
            
            # Get flags and notes
            flags = claim.flags.all().order_by('-flagged_at')
            notes = claim.notes.all().order_by('-created_at')
            
            context = {
                'claim': claim,
                'claim_details': claim_details,
                'total_billed': total_billed,
                'total_paid': total_paid,
                'total_allowed': total_allowed,
                'flags': flags,
                'notes': notes,
            }
            return render(request, 'claims/claim_detail_partial.html', context)
        return redirect('claims:claim_detail', claim_id=claim_id)
    
    return redirect('claims:claim_detail', claim_id=claim_id)

@login_required
def resolve_flag(request, flag_id):
    """Resolve a flag"""
    if request.method == 'POST':
        flag = get_object_or_404(ClaimFlag, id=flag_id)
        
        # Only allow resolving if flag is not already resolved
        if not flag.is_resolved:
            flag.is_resolved = True
            flag.resolved_at = timezone.now()
            flag.resolved_by = request.user
            flag.save()
        else:
            messages.info(request, 'This flag is already resolved.')
        
        if request.headers.get('HX-Request'):
            # Return the updated claim detail partial for HTMX
            claim = get_object_or_404(ClaimList, id=flag.claim.id)
            claim_details = ClaimDetail.objects.filter(claim_id=flag.claim.id)
            
            # Calculate totals
            total_billed = claim.billed_amount or 0
            total_paid = claim.paid_amount or 0
            total_allowed = total_paid
            
            # Get flags and notes
            flags = claim.flags.all().order_by('-flagged_at')
            notes = claim.notes.all().order_by('-created_at')
            
            context = {
                'claim': claim,
                'claim_details': claim_details,
                'total_billed': total_billed,
                'total_paid': total_paid,
                'total_allowed': total_allowed,
                'flags': flags,
                'notes': notes,
            }
            return render(request, 'claims/claim_detail_partial.html', context)
        return redirect('claims:claim_detail', claim_id=flag.claim.id)
    
    return redirect('claims:claim_detail', claim_id=flag.claim.id)

@login_required
def delete_note(request, note_id):
    """Delete a note"""
    if request.method == 'POST':
        note = get_object_or_404(ClaimNote, id=note_id)
        claim_id = note.claim.id
        
        # Only allow deletion if user owns the note or is admin
        if request.user == note.user or request.user.is_superuser:
            note.delete()
        else:
            messages.error(request, 'You can only delete your own notes.')
        
        return redirect('claims:claim_detail', claim_id=claim_id)
    
    return redirect('claims:claim_detail', claim_id=note.claim.id)

@login_required
def edit_note(request, note_id):
    """Edit a note"""
    note = get_object_or_404(ClaimNote, id=note_id)
    
    # Only allow editing if user owns the note or is admin
    if request.user != note.user and not request.user.is_superuser:
        messages.error(request, 'You can only edit your own notes.')
        return redirect('claims:claim_detail', claim_id=note.claim.id)
    
    if request.method == 'POST':
        note_text = request.POST.get('note', '').strip()
        
        if note_text:
            note.note = note_text
            note.save()
        else:
            messages.error(request, 'Note cannot be empty.')
        
        return redirect('claims:claim_detail', claim_id=note.claim.id)
    
    # For GET request, show edit form
    context = {
        'note': note,
        'claim': note.claim,
    }
    return render(request, 'claims/edit_note.html', context)

@login_required
def delete_flag(request, flag_id):
    """Delete a flag"""
    if request.method == 'POST':
        flag = get_object_or_404(ClaimFlag, id=flag_id)
        claim_id = flag.claim.id
        
        # Only allow deletion if user owns the flag or is admin
        if request.user == flag.user or request.user.is_superuser:
            flag.delete()
        else:
            messages.error(request, 'You can only delete your own flags.')
        
        return redirect('claims:claim_detail', claim_id=claim_id)
    
    return redirect('claims:claim_detail', claim_id=flag.claim.id)

def signup(request):
    """User signup view"""
    try:
        if request.user.is_authenticated:
            # If user is already logged in, redirect to dashboard
            return redirect('claims:dashboard')
        
        if request.method == 'POST':
            form = UserSignUpForm(request.POST)
            if form.is_valid():
                try:
                    # Create the user
                    user = form.save(commit=False)
                    
                    # Ensure email is saved (Django User model requires this)
                    user.email = form.cleaned_data['email']
                    user.save()
                    
                    # Log the user in
                    login(request, user)
                    
                    # Redirect to dashboard
                    return redirect('claims:dashboard')
                except Exception as e:
                    # Handle any errors during user creation
                    if 'user' in locals():
                        user.delete()
                    # Add the error to form errors
                    form.add_error(None, f'An error occurred while creating your account: {str(e)}')
                    return render(request, 'registration/signup.html', {'form': form})
            # If form is invalid, render with errors
            return render(request, 'registration/signup.html', {'form': form})
        else:
            # GET request - show empty form
            form = UserSignUpForm()
        
        return render(request, 'registration/signup.html', {'form': form})
    except Exception as e:
        # Catch any unexpected errors
        form = UserSignUpForm()
        form.add_error(None, f'An unexpected error occurred: {str(e)}')
        return render(request, 'registration/signup.html', {'form': form})
