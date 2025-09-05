from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid
from django.db import models
from django.utils import timezone
import random
from django.utils.text import slugify

# Create your models here.
class user_wallet(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    total_balance = models.CharField(max_length=200, default='0.00', null=False, blank=False)
    loans = models.CharField(max_length=200, default='0.00', null=False, blank=False)
    unverified = models.CharField(max_length=200, default='0.00', null=False, blank=False)
    bonus = models.CharField(max_length=200, default='0.00', null=False, blank=False)
    


    def __str__(self):
        return str(self.user)

class TransactionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255)




class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('transfer', 'Transfer'),
        ('withdraw', 'Withdraw'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=255, unique=True, editable=False)  # ✅ Make unique
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    recipient_account_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_transactions'
    )

    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # ✅ Generate a unique transaction_id if it's not set
        if not self.transaction_id:
            self.transaction_id = "TXN-" + uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ${self.amount} - {self.status}"

   

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imf_code = models.CharField(max_length=20, blank=True, null=True)
    cot_code = models.CharField(max_length=20, blank=True, null=True)
    tax_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username



DOCUMENT_TYPES = [
    ('NIN', 'National Identity Number'),
    ('PASSPORT', 'International Passport'),
    ('DL', 'Driver’s License'),
    ('PVC', 'Voter’s Card'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    # Personal info
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)

    # KYC fields
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, blank=True, null=True)
    id_front = models.ImageField(upload_to="kyc_documents/front/", blank=True, null=True)
    id_back = models.ImageField(upload_to="kyc_documents/back/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"


DOCUMENT_TYPES = [
    ('national_id', 'National ID'),
    ('passport', 'Passport'),
    ('driver_license', 'Driver’s License'),
    ('voter_card', 'Voter’s Card'),
    ('other', 'Other'),
]

KYC_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class KYC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    front_image = models.ImageField(upload_to="kyc/front/")
    back_image = models.ImageField(upload_to="kyc/back/")
    status = models.CharField(max_length=10, choices=KYC_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()} ({self.status})"


CARD_TYPES = [
    ('debit', 'Debit Card'),
    ('credit', 'Credit Card'),
    ('prepaid', 'Prepaid Card'),
]

DELIVERY_METHODS = [
    ('pickup', 'Pick Up at Branch'),
    ('home_delivery', 'Home Delivery'),
]

ATM_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class ATMCardApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS)
    id_proof = models.FileField(upload_to="atm/id_proofs/")
    status = models.CharField(max_length=10, choices=ATM_STATUS, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_name} - {self.get_card_type_display()} ({self.status})"




class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            # Generate a unique 10-digit account number
            while True:
                acc_num = str(random.randint(1000000000, 9999999999))
                if not BankAccount.objects.filter(account_number=acc_num).exists():
                    self.account_number = acc_num
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, default="Bank Transfer")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"
