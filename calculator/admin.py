from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile,
    Policy,
    Payment,
    Claim,
    PremiumCalculation,
    HealthCalculation,
    LifeCalculation,
    PropertyCalculation,
    VehicleCalculation, 
    Blog, 
    Contact , 
)


admin.site.register(Blog)
admin.site.register(Contact)


# -----------------------------
# USER PROFILE ADMIN
# -----------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'cnic', 'city', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'cnic']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Contact Details', {'fields': ('phone', 'address', 'city')}),
        ('Personal Information', {'fields': ('cnic', 'date_of_birth', 'profile_picture')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


# -----------------------------
# POLICY ADMIN
# -----------------------------
@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = [
        'policy_number', 'user', 'insurance_type', 'status',
        'monthly_premium', 'coverage_amount', 'start_date', 'end_date'
    ]
    list_filter = ['insurance_type', 'status', 'created_at']
    search_fields = ['policy_number', 'user__username', 'user__email']
    readonly_fields = ['policy_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Policy Information', {'fields': ('policy_number', 'user', 'insurance_type', 'status')}),
        ('Premium Details', {'fields': ('monthly_premium', 'yearly_premium', 'coverage_amount')}),
        ('Duration', {'fields': ('start_date', 'end_date')}),
        ('Additional Data', {'fields': ('policy_data',), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# -----------------------------
# PAYMENT ADMIN
# -----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'user', 'policy', 'amount',
        'payment_method', 'payment_status', 'payment_date'
    ]
    list_filter = ['payment_method', 'payment_status', 'payment_date']
    search_fields = ['transaction_id', 'user__username', 'policy__policy_number']
    readonly_fields = ['transaction_id', 'payment_date']
    date_hierarchy = 'payment_date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'policy')


# -----------------------------
# CLAIM ADMIN
# -----------------------------
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = [
        'claim_number', 'user', 'policy', 'claim_amount',
        'status_badge', 'incident_date', 'submitted_at'
    ]
    list_filter = ['status', 'submitted_at', 'incident_date']
    search_fields = ['claim_number', 'user__username', 'policy__policy_number']
    readonly_fields = ['claim_number', 'submitted_at', 'updated_at']
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('Claim Information', {'fields': ('claim_number', 'policy', 'user', 'status')}),
        ('Claim Details', {'fields': ('claim_amount', 'incident_date', 'incident_description')}),
        ('Documents', {'fields': ('document1', 'document2', 'document3')}),
        ('Review', {'fields': ('approved_amount', 'admin_notes')}),
        ('Timestamps', {'fields': ('submitted_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def status_badge(self, obj):
        colors = {
            'submitted': '#3b82f6',
            'under_review': '#f59e0b',
            'approved': '#10b981',
            'rejected': '#ef4444',
            'settled': '#8b5cf6'
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 15px; '
            'border-radius: 15px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'policy')


# -----------------------------
# PREMIUM CALCULATION ADMIN
# -----------------------------
@admin.register(PremiumCalculation)
class PremiumCalculationAdmin(admin.ModelAdmin):
    list_display = ['insurance_type', 'user', 'calculated_premium', 'created_at']
    list_filter = ['insurance_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# -----------------------------
# HEALTH CALCULATION ADMIN
# -----------------------------
@admin.register(HealthCalculation)
class HealthCalculationAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'city', 'bmi', 'smoker', 'premium', 'created_at']
    list_filter = ['gender', 'city', 'smoker', 'created_at']
    search_fields = ['user__username', 'city']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# -----------------------------
# LIFE CALCULATION ADMIN
# -----------------------------
@admin.register(LifeCalculation)
class LifeCalculationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'age', 'gender', 'smoker',
        'occupation_risk', 'coverage_amount', 'premium', 'created_at'
    ]
    list_filter = ['gender', 'smoker', 'occupation_risk', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# -----------------------------
# PROPERTY CALCULATION ADMIN
# -----------------------------
@admin.register(PropertyCalculation)
class PropertyCalculationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'property_type', 'city', 'property_value',
        'construction_year', 'premium', 'created_at'
    ]
    list_filter = ['property_type', 'city', 'fire_safety', 'created_at']
    search_fields = ['user__username', 'city', 'property_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# -----------------------------
# VEHICLE CALCULATION ADMIN
# -----------------------------
@admin.register(VehicleCalculation)
class VehicleCalculationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'vehicle_type', 'vehicle_value', 'driver_age',
        'city', 'claims_history', 'premium', 'created_at'
    ]
    list_filter = ['vehicle_type', 'city', 'created_at']
    search_fields = ['user__username', 'city', 'vehicle_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
