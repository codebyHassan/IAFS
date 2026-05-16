from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    HealthCalculatorForm, 
    LifeCalculatorForm,
    PropertyCalculatorForm,
    VehicleCalculatorForm
)
from .models import (
    HealthCalculation,
    LifeCalculation,
    PropertyCalculation,
    VehicleCalculation,
    PremiumCalculation
)
from .ml_models import (
    HealthPremiumModel,
    LifePremiumModel,
    PropertyPremiumModel,
    VehiclePremiumModel
)
import json

def home(request):
    """Home page with all insurance options"""
    context = {
        'total_calculations': PremiumCalculation.objects.count(),
        'health_calculations': HealthCalculation.objects.count(),
        'life_calculations': LifeCalculation.objects.count(),
        'property_calculations': PropertyCalculation.objects.count(),
        'vehicle_calculations': VehicleCalculation.objects.count(),
    }
    return render(request, 'calculator/home.html', context)


def health_calculator(request):
    """Health insurance premium calculator"""
    if request.method == 'POST':
        form = HealthCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Initialize model
            model = HealthPremiumModel()
            
            # Calculate premium
            result = model.calculate_premium(
                age=data['age'],
                gender=data['gender'],
                city=data['city'],
                height=data['height'],
                weight=data['weight'],
                smoker=data['smoker'],
                pre_existing_conditions=data['pre_existing_conditions'],
                coverage_amount=data['coverage_amount']
            )
            
            # Save to database
            calculation = HealthCalculation.objects.create(
                age=data['age'],
                gender=data['gender'],
                city=data['city'],
                bmi=result['bmi'],
                smoker=data['smoker'],
                pre_existing_conditions=data['pre_existing_conditions'],
                coverage_amount=data['coverage_amount'],
                premium=result['monthly_premium']
            )
            
            # Save to general calculation table
            PremiumCalculation.objects.create(
                insurance_type='health',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            # Store result in session
            request.session['calculation_result'] = {
                'type': 'Health Insurance',
                'icon': 'fa-heartbeat',
                'result': result,
                'input_data': data
            }
            
            return redirect('result')
    else:
        form = HealthCalculatorForm()
    
    return render(request, 'calculator/health_calculator.html', {'form': form})


def life_calculator(request):
    """Life insurance premium calculator"""
    if request.method == 'POST':
        form = LifeCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Initialize model
            model = LifePremiumModel()
            
            # Calculate premium
            result = model.calculate_premium(
                age=data['age'],
                gender=data['gender'],
                smoker=data['smoker'],
                occupation_risk=data['occupation_risk'],
                coverage_amount=data['coverage_amount'],
                policy_term=data['policy_term']
            )
            
            # Save to database
            calculation = LifeCalculation.objects.create(
                age=data['age'],
                gender=data['gender'],
                smoker=data['smoker'],
                occupation_risk=int(data['occupation_risk']),
                coverage_amount=data['coverage_amount'],
                policy_term=data['policy_term'],
                premium=result['monthly_premium']
            )
            
            # Save to general calculation table
            PremiumCalculation.objects.create(
                insurance_type='life',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            # Store result in session
            request.session['calculation_result'] = {
                'type': 'Life Insurance',
                'icon': 'fa-user-shield',
                'result': result,
                'input_data': data
            }
            
            return redirect('result')
    else:
        form = LifeCalculatorForm()
    
    return render(request, 'calculator/life_calculator.html', {'form': form})


def property_calculator(request):
    """Property insurance premium calculator"""
    if request.method == 'POST':
        form = PropertyCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Initialize model
            model = PropertyPremiumModel()
            
            # Calculate premium
            result = model.calculate_premium(
                property_value=data['property_value'],
                property_type=data['property_type'],
                city=data['city'],
                construction_year=data['construction_year'],
                security_features=data['security_features'],
                fire_safety=data['fire_safety']
            )
            
            # Save to database
            calculation = PropertyCalculation.objects.create(
                property_value=data['property_value'],
                property_type=data['property_type'],
                city=data['city'],
                construction_year=data['construction_year'],
                security_features=int(data['security_features']),
                fire_safety=data['fire_safety'],
                premium=result['monthly_premium']
            )
            
            # Save to general calculation table
            PremiumCalculation.objects.create(
                insurance_type='property',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            # Store result in session
            request.session['calculation_result'] = {
                'type': 'Property Insurance',
                'icon': 'fa-home',
                'result': result,
                'input_data': data
            }
            
            return redirect('result')
    else:
        form = PropertyCalculatorForm()
    
    return render(request, 'calculator/property_calculator.html', {'form': form})


def vehicle_calculator(request):
    """Vehicle insurance premium calculator"""
    if request.method == 'POST':
        form = VehicleCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Initialize model
            model = VehiclePremiumModel()
            
            # Calculate premium
            result = model.calculate_premium(
                vehicle_value=data['vehicle_value'],
                vehicle_type=data['vehicle_type'],
                vehicle_age=data['vehicle_age'],
                city=data['city'],
                driver_age=data['driver_age'],
                driver_experience=data['driver_experience'],
                claims_history=data['claims_history']
            )
            
            # Save to database
            calculation = VehicleCalculation.objects.create(
                vehicle_value=data['vehicle_value'],
                vehicle_type=data['vehicle_type'],
                vehicle_age=data['vehicle_age'],
                city=data['city'],
                driver_age=data['driver_age'],
                driver_experience=data['driver_experience'],
                claims_history=data['claims_history'],
                premium=result['monthly_premium']
            )
            
            # Save to general calculation table
            PremiumCalculation.objects.create(
                insurance_type='vehicle',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            # Store result in session
            request.session['calculation_result'] = {
                'type': 'Vehicle Insurance',
                'icon': 'fa-car',
                'result': result,
                'input_data': data
            }
            
            return redirect('result')
    else:
        form = VehicleCalculatorForm()
    
    return render(request, 'calculator/vehicle_calculator.html', {'form': form})


def result(request):
    """Display calculation result"""
    calculation_result = request.session.get('calculation_result')
    
    if not calculation_result:
        messages.warning(request, 'No calculation found. Please fill the form first.')
        return redirect('index')
    
    return render(request, 'calculator/result.html', {
        'calculation': calculation_result
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count, Sum
import stripe 
import json

from .forms import *
from .models import *
from .ml_models import *
from django.conf import settings

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# ==================== Authentication Views ====================

def register_view(request):
    """User Registration"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                cnic=form.cleaned_data['cnic'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'calculator/auth/register.html', {'form': form})


def login_view(request):
    """User Login"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('user_dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'calculator/auth/login.html', {'form': form})


def logout_view(request):
    """User Logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def profile_view(request):
    """User Profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'calculator/auth/profile.html', context)


# ==================== Calculator Views (Updated) ====================

def home(request):
    """Home page"""
    context = {
        'total_calculations': PremiumCalculation.objects.count(),
        'health_calculations': HealthCalculation.objects.count(),
        'life_calculations': LifeCalculation.objects.count(),
        'property_calculations': PropertyCalculation.objects.count(),
        'vehicle_calculations': VehicleCalculation.objects.count(),
    }
    return render(request, 'calculator/home.html', context)


def health_calculator(request):
    """Health insurance calculator"""
    if request.method == 'POST':
        form = HealthCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Initialize model and calculate premium
            model = HealthPremiumModel()
            result = model.calculate_premium(
                age=data['age'],
                gender=data['gender'],
                city=data['city'],
                height=data['height'],
                weight=data['weight'],
                smoker=data['smoker'],
                pre_existing_conditions=data['pre_existing_conditions'],
                coverage_amount=data['coverage_amount']
            )
            
            # Save calculation
            calculation = HealthCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                age=data['age'],
                gender=data['gender'],
                city=data['city'],
                bmi=result['bmi'],
                smoker=data['smoker'],
                pre_existing_conditions=data['pre_existing_conditions'],
                coverage_amount=data['coverage_amount'],
                premium=result['monthly_premium']
            )
            
            PremiumCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                insurance_type='health',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            # Store result in session
            request.session['calculation_result'] = {
                'type': 'Health Insurance',
                'icon': 'fa-heartbeat',
                'result': result,
                'input_data': data,
                'insurance_type': 'health'
            }
            
            return redirect('result')
    else:
        form = HealthCalculatorForm()
    
    return render(request, 'calculator/health_calculator.html', {'form': form})


# Similar updates for life, property, vehicle calculators...
def life_calculator(request):
    """Life insurance calculator"""
    if request.method == 'POST':
        form = LifeCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            model = LifePremiumModel()
            result = model.calculate_premium(
                age=data['age'],
                gender=data['gender'],
                smoker=data['smoker'],
                occupation_risk=data['occupation_risk'],
                coverage_amount=data['coverage_amount'],
                policy_term=data['policy_term']
            )
            
            LifeCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                age=data['age'],
                gender=data['gender'],
                smoker=data['smoker'],
                occupation_risk=int(data['occupation_risk']),
                coverage_amount=data['coverage_amount'],
                policy_term=data['policy_term'],
                premium=result['monthly_premium']
            )
            
            PremiumCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                insurance_type='life',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            request.session['calculation_result'] = {
                'type': 'Life Insurance',
                'icon': 'fa-user-shield',
                'result': result,
                'input_data': data,
                'insurance_type': 'life'
            }
            
            return redirect('result')
    else:
        form = LifeCalculatorForm()
    
    return render(request, 'calculator/life_calculator.html', {'form': form})


def property_calculator(request):
    """Property insurance calculator"""
    if request.method == 'POST':
        form = PropertyCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            model = PropertyPremiumModel()
            result = model.calculate_premium(
                property_value=data['property_value'],
                property_type=data['property_type'],
                city=data['city'],
                construction_year=data['construction_year'],
                security_features=data['security_features'],
                fire_safety=data['fire_safety']
            )
            
            PropertyCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                property_value=data['property_value'],
                property_type=data['property_type'],
                city=data['city'],
                construction_year=data['construction_year'],
                security_features=int(data['security_features']),
                fire_safety=data['fire_safety'],
                premium=result['monthly_premium']
            )
            
            PremiumCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                insurance_type='property',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            request.session['calculation_result'] = {
                'type': 'Property Insurance',
                'icon': 'fa-home',
                'result': result,
                'input_data': data,
                'insurance_type': 'property'
            }
            
            return redirect('result')
    else:
        form = PropertyCalculatorForm()
    
    return render(request, 'calculator/property_calculator.html', {'form': form})


def vehicle_calculator(request):
    """Vehicle insurance calculator"""
    if request.method == 'POST':
        form = VehicleCalculatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            model = VehiclePremiumModel()
            result = model.calculate_premium(
                vehicle_value=data['vehicle_value'],
                vehicle_type=data['vehicle_type'],
                vehicle_age=data['vehicle_age'],
                city=data['city'],
                driver_age=data['driver_age'],
                driver_experience=data['driver_experience'],
                claims_history=data['claims_history']
            )
            
            VehicleCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                vehicle_value=data['vehicle_value'],
                vehicle_type=data['vehicle_type'],
                vehicle_age=data['vehicle_age'],
                city=data['city'],
                driver_age=data['driver_age'],
                driver_experience=data['driver_experience'],
                claims_history=data['claims_history'],
                premium=result['monthly_premium']
            )
            
            PremiumCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                insurance_type='vehicle',
                calculated_premium=result['monthly_premium'],
                input_data=data
            )
            
            request.session['calculation_result'] = {
                'type': 'Vehicle Insurance',
                'icon': 'fa-car',
                'result': result,
                'input_data': data,
                'insurance_type': 'vehicle'
            }
            
            return redirect('result')
    else:
        form = VehicleCalculatorForm()
    
    return render(request, 'calculator/vehicle_calculator.html', {'form': form})


def result(request):
    """Display calculation result"""
    calculation_result = request.session.get('calculation_result')
    
    if not calculation_result:
        messages.warning(request, 'No calculation found. Please fill the form first.')
        return redirect('index')
    
    return render(request, 'calculator/result.html', {
        'calculation': calculation_result
    })


# ==================== Policy Purchase Views ====================

@login_required
def buy_policy(request):
    """Buy insurance policy"""
    calculation_result = request.session.get('calculation_result')
    
    if not calculation_result:
        messages.warning(request, 'Please calculate premium first.')
        return redirect('index')
    
    if request.method == 'POST':
        # Create policy
        result = calculation_result['result']
        data = calculation_result['input_data']
        
        # Determine coverage amount based on insurance type
        coverage_amount = data.get('coverage_amount', result.get('coverage_amount', 0))
        
        policy = Policy.objects.create(
            user=request.user,
            insurance_type=calculation_result['insurance_type'],
            monthly_premium=result['monthly_premium'],
            yearly_premium=result['yearly_premium'],
            coverage_amount=coverage_amount,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365),
            policy_data=data,
            status='pending'
        )
        
        # Store policy ID in session for payment
        request.session['pending_policy_id'] = policy.id
        
        return redirect('payment_page', policy_id=policy.id)
    
    return render(request, 'calculator/policy/buy_policy.html', {
        'calculation': calculation_result
    })


@login_required
def payment_page(request, policy_id):
    """Payment page"""
    policy = get_object_or_404(Policy, id=policy_id, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'stripe':
            try:
                # Create Stripe payment intent
                intent = stripe.PaymentIntent.create(
                    amount=int(policy.yearly_premium * 100),  # Convert to cents
                    currency='pkr',
                    metadata={'policy_id': policy.id}
                )
                
                # Create payment record
                payment = Payment.objects.create(
                    transaction_id=intent.id,
                    policy=policy,
                    user=request.user,
                    amount=policy.yearly_premium,
                    payment_method='stripe',
                    payment_status='completed',
                    stripe_charge_id=intent.id
                )
                
                # Update policy status
                policy.status = 'active'
                policy.save()
                
                # Clear session
                if 'calculation_result' in request.session:
                    del request.session['calculation_result']
                if 'pending_policy_id' in request.session:
                    del request.session['pending_policy_id']
                
                messages.success(request, 'Payment successful! Your policy is now active.')
                return redirect('payment_success', payment_id=payment.id)
                
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment failed: {str(e)}')
                
        else:
            # Demo payment for JazzCash/EasyPaisa
            import uuid
            transaction_id = f'TXN{uuid.uuid4().hex[:12].upper()}'
            
            payment = Payment.objects.create(
                transaction_id=transaction_id,
                policy=policy,
                user=request.user,
                amount=policy.yearly_premium,
                payment_method=payment_method,
                payment_status='completed'
            )
            
            policy.status = 'active'
            policy.save()
            
            if 'calculation_result' in request.session:
                del request.session['calculation_result']
            if 'pending_policy_id' in request.session:
                del request.session['pending_policy_id']
            
            messages.success(request, 'Payment successful! Your policy is now active.')
            return redirect('payment_success', payment_id=payment.id)
    
    context = {
        'policy': policy,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'calculator/policy/payment.html', context)


@login_required
def payment_success(request, payment_id):
    """Payment success page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'calculator/policy/payment_success.html', {
        'payment': payment,
        'policy': payment.policy
    })


@login_required
def policy_detail(request, policy_id):
    """View policy details"""
    policy = get_object_or_404(Policy, id=policy_id, user=request.user)
    return render(request, 'calculator/policy/policy_detail.html', {'policy': policy})


# ==================== Dashboard Views ====================

@login_required
def user_dashboard(request):
    """User dashboard"""
    policies = Policy.objects.filter(user=request.user)
    claims = Claim.objects.filter(user=request.user)
    
    context = {
        'total_policies': policies.count(),
        'active_policies': policies.filter(status='active').count(),
        'total_claims': claims.count(),
        'pending_claims': claims.filter(status='submitted').count(),
        'recent_policies': policies[:5],
        'recent_claims': claims[:5],
    }
    return render(request, 'calculator/dashboard/user_dashboard.html', context)


@login_required
def my_policies(request):
    """View all user policies"""
    policies = Policy.objects.filter(user=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        policies = policies.filter(status=status_filter)
    
    context = {
        'policies': policies,
        'status_filter': status_filter,
    }
    return render(request, 'calculator/dashboard/my_policies.html', context)


@login_required
def my_claims(request):
    """View all user claims"""
    claims = Claim.objects.filter(user=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        claims = claims.filter(status=status_filter)
    
    context = {
        'claims': claims,
        'status_filter': status_filter,
    }
    return render(request, 'calculator/dashboard/my_claims.html', context)


# ==================== Claims Views ====================

@login_required
def submit_claim(request, policy_id):
    """Submit insurance claim"""
    policy = get_object_or_404(Policy, id=policy_id, user=request.user)
    
    if policy.status != 'active':
        messages.error(request, 'You can only claim on active policies.')
        return redirect('my_policies')
    
    if request.method == 'POST':
        form = ClaimSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.policy = policy
            claim.user = request.user
            claim.save()
            
            messages.success(request, 'Claim submitted successfully! We will review it shortly.')
            return redirect('claim_detail', claim_id=claim.id)
    else:
        form = ClaimSubmissionForm()
    
    return render(request, 'calculator/claims/submit_claim.html', {
        'form': form,
        'policy': policy
    })


@login_required
def claim_detail(request, claim_id):
    """View claim details"""
    claim = get_object_or_404(Claim, id=claim_id, user=request.user)
    return render(request, 'calculator/claims/claim_detail.html', {'claim': claim})


# ==================== Admin Views ====================
@user_passes_test(lambda u: u.is_staff)
def admin_claims(request):
    claims = Claim.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        claims = claims.filter(status=status_filter)

    context = {
        'claims': claims,
        'status_filter': status_filter,
        'total_claims': Claim.objects.count(),
        'pending_claims': Claim.objects.filter(status='submitted').count(),
        'approved_claims': Claim.objects.filter(status='approved').count(),
        'rejected_claims': Claim.objects.filter(status='rejected').count(),
    }
    return render(request, 'calculator/dashboard/admin_claims.html', context)

@user_passes_test(lambda u: u.is_staff)
def review_claim(request, claim_id):
    """Review and update claim status"""
    claim = get_object_or_404(Claim, id=claim_id)
    
    if request.method == 'POST':
        form = ClaimReviewForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            messages.success(request, 'Claim updated successfully!')
            return redirect('admin_claims')
    else:
        form = ClaimReviewForm(instance=claim)
    
    return render(request, 'calculator/claims/review_claim.html', {
        'form': form,
        'claim': claim
    })



########################## INDEX PAGES ##################################


def index(request):
    return render(request , 'calculator/index.html')

def about(request):
     return render(request , 'calculator/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you for contacting us! We’ll get back to you soon.")
            return redirect('contact')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ContactForm()
    
    return render(request, 'calculator/contact.html', {'form': form})



def plans(request):
     return render(request , 'calculator/plans.html')


from .models import Blog

def blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'calculator/blog.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'calculator/blog_detail.html', {'blog': blog})