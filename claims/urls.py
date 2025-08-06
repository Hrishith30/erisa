from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<str:claim_id>/', views.claim_detail, name='claim_detail'),
    path('claims/<str:claim_id>/htmx/', views.claim_detail_htmx, name='claim_detail_htmx'),
    path('claims/<str:claim_id>/flag/', views.flag_claim, name='flag_claim'),
    path('claims/<str:claim_id>/note/', views.add_note, name='add_note'),
    path('flags/<int:flag_id>/resolve/', views.resolve_flag, name='resolve_flag'),
    path('flags/<int:flag_id>/delete/', views.delete_flag, name='delete_flag'),
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('claim-details/', views.claim_details_list, name='claim_details_list'),
    path('analytics/', views.analytics, name='analytics'),
    path('api/claims-data/', views.api_claims_data, name='api_claims_data'),
]
