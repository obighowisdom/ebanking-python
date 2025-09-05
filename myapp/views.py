from django.contrib import messages
from django.http import HttpResponse
from . forms import UserRegisterForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import TransactionForm
from .models import Transaction
from reportlab.pdfgen import canvas
from .forms import KYCForm
from reportlab.lib.pagesizes import letter
from .models import UserProfile, Profile
from django.contrib.auth import logout
from .models import KYC
from .forms import ATMCardApplicationForm
from .models import ATMCardApplication
from .models import BankAccount
from .forms import DepositForm
from .models import Deposit


from .models import user_wallet

# Create your views here.
def index(request):
   
    return render(request, 'home/home.html')


def current_accounts(request):
   
    return render(request, 'home/current-accounts.html')


def getting_started(request):
   
    return render(request, 'home/getting-started.html')

def premier_accounts(request):
   
    return render(request, 'home/premier-accounts.html')

def advance_accounts(request):
   
    return render(request, 'home/advance-accounts.html')

def student_accounts(request):
   
    return render(request, 'home/student-accounts.html')

def bank_accounts(request):
   
    return render(request, 'home/bank-accounts.html')

def loans(request):
   
    return render(request, 'home/loans.html')

def personal_loans(request):
   
    return render(request, 'home/personal-loans.html')

def car_loans(request):
   
    return render(request, 'home/car-loans.html')

def flexible(request):
   
    return render(request, 'home/flexible.html')

def premier_personal(request):
   
    return render(request, 'home/premier-personal.html')

def graduate_loans(request):
   
    return render(request, 'home/graduate-loans.html')

def overdrafts(request):
   
    return render(request, 'home/overdrafts.html')

def investing(request):
   
    return render(request, 'home/investing.html')

def investmet_funds(request):
   
    return render(request, 'home/investment-funds.html')

def branch_locator(request):
   
    return render(request, 'home/branch-locator.html')

def why_us(request):
   
    return render(request, 'home/why-invest-with-us.html')

def insurance(request):
   
    return render(request, 'home/insurance.html')

def home_insurance(request):
   
    return render(request, 'home/home-insurance.html')

def travel_insurance(request):
   
    return render(request, 'home/travel-insurance.html')

def student_insurance(request):
   
    return render(request, 'home/student-insurance.html')

def contactandsupport(request):
   
    return render(request, 'home/contactandsupport.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
                       
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect("index:login")
    else:
        form = UserRegisterForm()
   
    return render(request, 'auth/register.html', {'form':form})

def privacy(request):
   
    return render(request, 'auth/privacy.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password1 = request.POST['password1']
        
#         user = authenticate(username=username, password=password1)
        
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             messages.success(request, "Logged In Sucessfully!!")
#             return render(request, "dashboard.html", {"fname":fname})
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect("index:login")
   
#     return render(request, 'auth/login.html')

# user dashboard

def dashboard(request):
    wallet = user_wallet.objects.all()
     
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'dashboard/dashboard.html', {
    "wallet": wallet,
    "transactions": transactions
})


def transfer(request):
   
    return render(request, 'dashboard/transfer.html')


# views.py


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.status = 'pending'  # Default status
            transaction.save()

            # If the request is AJAX, return JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Transaction submitted successfully! Pending IMF verification.'
                })

            # Fallback (normal form submit without AJAX)
            messages.success(request, 'Transaction submitted successfully! It is now pending admin approval.')
            return redirect('/transfer')

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                })

            messages.error(request, 'Please correct the errors below.')

    else:
        form = TransactionForm()

    # Render template for GET requests
    return render(request, 'dashboard/transfer.html', {'form': form})

@login_required
def user_transactions(request):
    """View for users to see their transaction history"""
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'user_transactions.html', {'transactions': transactions})

@login_required
def transaction_history(request):
    # Get all transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]  # Show last 10
    return render(request, 'dashboard/transaction_history.html', {'transactions': transactions})

@login_required
def transaction_detail(request, pk):
    # Get a specific transaction by ID
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'dashboard/transaction_detail.html', {'transaction': transaction})

def download_receipt(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    # Create PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=receipt_{transaction.transaction_id}.pdf"
    
    # Generate PDF content
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Transaction Receipt")

    # Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Transaction Receipt")

    # Details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 710, f"Transaction ID: {transaction.transaction_id}")
    pdf.drawString(50, 690, f"Transaction Type: {transaction.get_transaction_type_display()}")
    pdf.drawString(50, 670, f"Bank: {transaction.bank_name}")
    pdf.drawString(50, 650, f"Account Number: {transaction.account_number}")
    pdf.drawString(50, 630, f"Recipient Name: {transaction.recipient_account_name}")
    pdf.drawString(50, 610, f"Amount: ${transaction.amount}")
    pdf.drawString(50, 590, f"Status: {transaction.status.title()}")
    pdf.drawString(50, 570, f"Date: {transaction.created_at.strftime('%B %d, %Y %H:%M')}")

    pdf.showPage()
    pdf.save()

    return response


@login_required
def verify_code(request):
    if request.method == "POST":
        code_type = request.POST.get("code_type")  # 'imf', 'cot', or 'tax'
        code_entered = request.POST.get("code_value")

        # Get the user's profile
        profile = get_object_or_404(UserProfile, user=request.user)

        # Check based on code type
        if code_type == "imf":
            valid_code = profile.imf_code
        elif code_type == "cot":
            valid_code = profile.cot_code
        elif code_type == "tax":
            valid_code = profile.tax_code
        else:
            return JsonResponse({"success": False, "message": "Invalid code type."})

        # Compare codes
        if code_entered == valid_code:
            return JsonResponse({"success": True, "message": "Code verified successfully."})
        else:
            return JsonResponse({"success": False, "message": "Invalid code. Please try again."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # If profile is verified, do NOT allow editing
    if profile.is_verified:
        return render(request, "dashboard/profile.html", {"profile": profile, "locked": True})

    if request.method == "POST":
        # Update User fields
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update Profile fields
        profile.profile_photo = request.FILES.get("profile_photo", profile.profile_photo)
        profile.address = request.POST.get("address")
        profile.city = request.POST.get("city")
        profile.country = request.POST.get("country")
        profile.postal_code = request.POST.get("postal_code")
        profile.about_me = request.POST.get("about_me")
        profile.document_type = request.POST.get("document_type")

        if request.FILES.get("id_front"):
            profile.id_front = request.FILES["id_front"]
        if request.FILES.get("id_back"):
            profile.id_back = request.FILES["id_back"]

        # ✅ Lock the profile after first update
        profile.is_verified = True
        profile.save()

        messages.success(request, "✅ Profile updated successfully! Your details are now locked.")
        return redirect("/profile")

    return render(request, "dashboard/profile.html", {"profile": profile})

def custom_logout(request):
    logout(request)
    messages.success(request, "✅ You have been signed out successfully!")
    return redirect('/login')  # Replace 'login' with your login page name

@login_required
def kyc(request):
    # Check if the user has already submitted KYC
    existing_kyc = KYC.objects.filter(user=request.user).first()

    if request.method == "POST" and not existing_kyc:
        form = KYCForm(request.POST, request.FILES)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.status = "pending"
            kyc.save()
            messages.success(request, "✅ KYC documents uploaded successfully! Waiting for admin approval.")
            return redirect("/kyc")
        else:
            messages.error(request, "❌ There was an error uploading your documents. Please try again.")
    else:
        form = KYCForm()

    return render(request, "dashboard/kyc.html", {
        "form": form,
        "existing_kyc": existing_kyc
    })


def atm(request):
    # Check if the user has already applied
    existing_application = ATMCardApplication.objects.filter(user=request.user).first()

    if request.method == "POST" and not existing_application:
        form = ATMCardApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            atm = form.save(commit=False)
            atm.user = request.user
            atm.status = "pending"
            atm.save()
            messages.success(request, "✅ Your ATM card application has been submitted successfully! Waiting for approval.")
            return redirect("/atm")
        else:
            messages.error(request, "❌ There was an error submitting your application. Please try again.")
    else:
        form = ATMCardApplicationForm()

    return render(request, "dashboard/atm.html", {
        "form": form,
        "existing_application": existing_application
    })



@login_required
def generate_account_number(request):
    user = request.user

    # Check if user already has an account number
    account = BankAccount.objects.filter(user=user).first()
    if account:
        return JsonResponse({
            "status": "exists",
            "account_number": account.account_number,
            "message": "You already have an account number."
        })

    # Check if profile is incomplete
    if not user.first_name or user.first_name.strip() == "":
        return JsonResponse({"status": "error", "message": "Please update your profile first."})

    # Create a new account number
    account = BankAccount.objects.create(user=user)

    return JsonResponse({
        "status": "success",
        "account_number": account.account_number,
        "message": "Account number generated successfully!"
    })


@login_required
def deposit(request):
    # Get the latest deposit request if exists
    existing_deposit = Deposit.objects.filter(user=request.user).order_by('-created_at').first()

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()
            messages.success(request, "Deposit request submitted successfully and is pending approval.")
            return redirect('/deposit')  # Redirect to the same page
    else:
        form = DepositForm()

    return render(request, 'dashboard/deposit.html', {
        'form': form,
        'existing_deposit': existing_deposit
    })
