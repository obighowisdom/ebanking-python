from django.contrib import admin

# Register your models here.
from .models import user_wallet
from django.utils.html import format_html
from .models import Transaction
from .models import UserProfile, Profile, BankAccount
from .models import KYC
from django.contrib import admin
from .models import Deposit

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'imf_code', 'cot_code', 'tax_code')
    search_fields = ('user__username', 'imf_code', 'cot_code', 'tax_code')

admin.site.register(UserProfile, UserProfileAdmin)


admin.site.register(user_wallet)
admin.site.register(Profile)
admin.site.register(BankAccount)

# admin.py

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'transaction_type', 
        'account_number',
        'bank_name', 
        'amount', 
        'status_badge', 
        'created_at'
    ]
    list_filter = [
        'status', 
        'transaction_type', 
        'bank_name', 
        'created_at'
    ]
    search_fields = [
        'user__username', 
        'user__email', 
        'account_number', 
        'recipient_account_name'
    ]
    readonly_fields = [
        'user', 
        'transaction_type', 
        'bank_name', 
        'account_number', 
        'recipient_account_name', 
        'amount', 
        'remark', 
        'created_at'
    ]
    fields = [
        'user',
        'transaction_type',
        'bank_name',
        'account_number',
        'recipient_account_name',
        'amount',
        'remark',
        'status',
        'processed_by',
        'created_at',
        'updated_at'
    ]
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if change:  # If updating existing transaction
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing transaction
            return self.readonly_fields + ('updated_at',)
        return self.readonly_fields
    
    def has_add_permission(self, request):
        # Admins shouldn't create transactions directly
        return False
    
    actions = ['approve_transactions', 'reject_transactions']
    
    def approve_transactions(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            processed_by=request.user
        )
        self.message_user(request, f'{updated} transactions have been approved.')
    approve_transactions.short_description = 'Approve selected transactions'
    
    def reject_transactions(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            processed_by=request.user
        )
        self.message_user(request, f'{updated} transactions have been rejected.')
    reject_transactions.short_description = 'Reject selected transactions'


admin.site.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ("user", "document_type", "status", "submitted_at")
    list_filter = ("status", "document_type")
    search_fields = ("user__username", "document_type")
    ordering = ("-submitted_at",)



@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'amount')
    ordering = ('-created_at',)
