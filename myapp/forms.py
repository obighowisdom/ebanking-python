from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Transaction
from .models import KYC
from .models import Profile
from .models import ATMCardApplication
from .models import Deposit


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "text",
        "placeholder": " enter username", 
    }), label="Username")

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "email",
        "placeholder": " enter email ", 
    }))
    
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "password",
        "placeholder": " enter password ", 
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form--control",
        "type": "password",
        "placeholder": " re-enter password ", 
    }))


    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']




class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'transaction_type', 
            'bank_name', 
            'account_number', 
            'recipient_account_name', 
            'amount', 
            'remark'
        ]
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
    
    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if account_number and len(account_number) < 5:
            raise forms.ValidationError("Account number must be at least 5 characters long.")
        return account_number


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_photo",
            "first_name",
            "last_name",
            "address",
            "city",
            "country",
            "postal_code",
            "about_me",
            "document_type",
            "id_front",
            "id_back",
        ]



class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['document_type', 'front_image', 'back_image']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'front_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
            'back_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
        }



class ATMCardApplicationForm(forms.ModelForm):
    class Meta:
        model = ATMCardApplication
        fields = ['account_number', 'account_name', 'card_type', 'delivery_method', 'id_proof']
        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your account number'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your account name'}),
            'card_type': forms.Select(attrs={'class': 'form-select'}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
        }


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'required': 'required'
            }),
        }
