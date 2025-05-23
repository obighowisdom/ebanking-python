from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from . forms import UserRegisterForm 
from django.contrib.auth.forms import UserCreationForm

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
   
    return render(request, 'dashboard/dashboard.html', {"wallet":wallet})


def transfer(request):
   
    return render(request, 'dashboard/transfer.html')
