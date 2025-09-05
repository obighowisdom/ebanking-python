from django.urls import path
from . import views
from django.contrib.auth import views as auth_view


app_name = 'myappurl'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('current-accounts/', views.current_accounts, name = 'current-accounts'),
    path('getting-started/', views.getting_started, name = 'getting-started'),
    path('premier-accounts/', views.premier_accounts, name = 'premier-accounts'),
    path('advance-accounts/', views.advance_accounts, name = 'advance-accounts'),
    path('student-accounts/', views.student_accounts, name = 'student-accounts'),
    path('bank-accounts/', views.bank_accounts, name = 'bank-accounts'),

    path('loans/', views.loans, name = 'loans'),
    path('personal-loans/', views.personal_loans, name = 'personal-loans'),
    path('car-loans/', views.car_loans, name = 'car-loans'),
    path('flexible/', views.flexible, name = 'flexible'),
    path('premier-personal/', views.premier_personal, name = 'premier-personal'),
    path('graduate-loans/', views.graduate_loans, name = 'graduate-loans'),
    path('overdrafts/', views.overdrafts, name = 'overdrafts'),

    path('investing/', views.investing, name = 'investing'),
    path('investment-funds/', views.investmet_funds, name = 'investment-funds'),
    path('branch-locator/', views.branch_locator, name = 'branch-locator'),
    path('why-invest-with-us/', views.why_us, name = 'why-invest-with-us'),

    path('insurance/', views.insurance, name = 'insurance'),
    path('home-insurance/', views.home_insurance, name = 'home-insurance'),
    path('travel-insurance/', views.travel_insurance, name = 'travel-insurance'),
    path('student-insurance/', views.student_insurance, name = 'student-insurance'),

    path('contactandsupport/', views.contactandsupport, name = 'contactandsupport'),

    # auth
    path('register/', views.register, name = 'register'),
    path('login/', auth_view.LoginView.as_view(template_name='auth/login.html'), name = 'login'),
    path('logout/', views.custom_logout, name='logout'),

    path('privacy/', views.privacy, name = 'privacy'),

    # dashboard

    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('transfer/', views.create_transaction, name='create_transaction'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path("transactions/<int:pk>/download/", views.download_receipt, name="download_receipt"),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('profile/', views.profile, name = 'profile'),
    path('kyc/', views.kyc, name = 'kyc'),
    path('atm/', views.atm, name = 'atm'),
    path('deposit/', views.deposit, name = 'deposit'),
    path("generate-account-number/", views.generate_account_number, name="generate_account_number"),














    # path('dashboard/', views.dash, name = 'dash'),

    # path('about/', views.about, name = 'about'),
    # path('login/', auth_view.LoginView.as_view(template_name='login.html'), name = 'login'),
    # path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name = 'logout'),




]