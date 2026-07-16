from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Transaction
from .models import KYC
from .models import Profile
from .models import ATMCardApplication
from .models import Deposit
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomerProfile


class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class":"form--control",
            "placeholder":"First Name"
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class":"form--control",
            "placeholder":"Last Name"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class":"form--control",
            "placeholder":"Username"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class":"form--control",
            "placeholder":"Email"
        })
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "class":"form--control",
            "placeholder":"Phone Number"
        })
    )

    country = forms.CharField(
    widget=forms.Select(attrs={
        "class":"form--control",
        "id":"country"
    })
    )

    state = forms.CharField(
        widget=forms.Select(attrs={
            "class":"form--control",
            "id":"state"
        })
    )

    city = forms.CharField(
        widget=forms.Select(attrs={
            "class":"form--control",
            "id":"city"
        })
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            "class":"form--control",
            "placeholder":"Residential Address"
        })
    )

    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            "class":"form--control",
            "type":"date"
        })
    )

    gender = forms.ChoiceField(
        choices=[
            ("","Select Gender"),
            ("Male","Male"),
            ("Female","Female"),
            ("Other","Other"),
        ],
        widget=forms.Select(attrs={
            "class":"form--control"
        })
    )

    account_type = forms.ChoiceField(
        choices=[
            ("","Select Account"),
            ("Savings","Savings"),
            ("Checking","Checking"),
            ("Current","Current"),
            ("Domiciliary","Domiciliary"),
        ],
        widget=forms.Select(attrs={
            "class":"form--control"
        })
    )

    preferred_branch = forms.ChoiceField(
        choices=[
            ("","Select Branch"),
            ("New York","New York"),
            ("California","California"),
            ("Texas","Texas"),
            ("Florida","Florida"),
            ("Illinois","Illinois"),
        ],
        widget=forms.Select(attrs={
            "class":"form--control"
        })
    )

    transfer_pin = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput(attrs={
            "class":"form--control",
            "maxlength":"4",
            "placeholder":"4-digit Transfer PIN"
        })
    )

    def clean_transfer_pin(self):
        pin = self.cleaned_data.get("transfer_pin")

        if not pin.isdigit():
            raise forms.ValidationError(
                "Transfer PIN must contain only numbers."
        )

        if len(pin) != 4:
            raise forms.ValidationError(
                "Transfer PIN must be exactly 4 digits."
            )

        return pin

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class":"form--control"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class":"form--control"
        })
    )

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "country",
            "state",
            "city",
            "address",
            "dob",
            "gender",
            "account_type",
            "preferred_branch",
            "transfer_pin",
            "password1",
            "password2",
        )




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



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomerProfile


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form--control",
            "placeholder": "Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form--control",
            "placeholder": "Password"
        })
    )

    def confirm_login_allowed(self, user):
        print("LOGIN CHECK:", user.username)

        super().confirm_login_allowed(user)

        profile = CustomerProfile.objects.get(user=user)

        if profile.status == "pending":
            raise ValidationError(
                "Your account is still pending review. Please wait for approval.",
                code="pending",
            )

        if profile.status == "rejected":
            raise ValidationError(
                "Your account has been rejected. Please contact customer support.",
                code="rejected",
            )