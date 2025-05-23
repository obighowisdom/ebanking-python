from django.db import models
from django.contrib.auth.models import User

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
   