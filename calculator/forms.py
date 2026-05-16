from django import forms
from .models import Contact

PAKISTANI_CITIES = [
    ('karachi', 'Karachi'),
    ('lahore', 'Lahore'),
    ('islamabad', 'Islamabad'),
    ('rawalpindi', 'Rawalpindi'),
    ('faisalabad', 'Faisalabad'),
    ('multan', 'Multan'),
    ('peshawar', 'Peshawar'),
    ('quetta', 'Quetta'),
    ('sialkot', 'Sialkot'),
    ('gujranwala', 'Gujranwala'),
]

class HealthCalculatorForm(forms.Form):
    age = forms.IntegerField(
        min_value=18, 
        max_value=80,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        label='Age (Years)'
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    
    height = forms.FloatField(
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Height in cm',
            'step': '0.1'
        }),
        label='Height (cm)'
    )
    
    weight = forms.FloatField(
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Weight in kg',
            'step': '0.1'
        }),
        label='Weight (kg)'
    )
    
    smoker = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Are you a smoker?'
    )
    
    pre_existing_conditions = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of conditions'
        }),
        label='Pre-existing Medical Conditions (Count)'
    )
    
    coverage_amount = forms.IntegerField(
        min_value=100000,
        max_value=10000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 500000'
        }),
        label='Desired Coverage Amount (PKR)'
    )


class LifeCalculatorForm(forms.Form):
    age = forms.IntegerField(
        min_value=18,
        max_value=70,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        label='Age (Years)'
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender'
    )
    
    smoker = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Are you a smoker?'
    )
    
    occupation_risk = forms.ChoiceField(
        choices=[
            (1, 'Low Risk (Office Work)'),
            (2, 'Moderate Risk (Teaching, Sales)'),
            (3, 'Medium Risk (Driver, Factory Worker)'),
            (4, 'High Risk (Construction, Mining)'),
            (5, 'Very High Risk (Military, Police)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Occupation Risk Level'
    )
    
    coverage_amount = forms.IntegerField(
        min_value=500000,
        max_value=50000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 5000000'
        }),
        label='Sum Assured (PKR)'
    )
    
    policy_term = forms.IntegerField(
        min_value=5,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 20'
        }),
        label='Policy Term (Years)'
    )


class PropertyCalculatorForm(forms.Form):
    property_value = forms.IntegerField(
        min_value=1000000,
        max_value=500000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 10000000'
        }),
        label='Property Value (PKR)'
    )
    
    property_type = forms.ChoiceField(
        choices=[
            ('house', 'Residential House'),
            ('apartment', 'Apartment/Flat'),
            ('commercial', 'Commercial Building'),
            ('shop', 'Shop'),
            ('warehouse', 'Warehouse'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Property Type'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    
    construction_year = forms.IntegerField(
        min_value=1950,
        max_value=2024,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2015'
        }),
        label='Year of Construction'
    )
    
    security_features = forms.ChoiceField(
        choices=[
            (0, 'No Security'),
            (1, 'Basic (Locks only)'),
            (2, 'Standard (Locks + Grills)'),
            (3, 'Good (+ Security Guard)'),
            (4, 'Excellent (+ CCTV)'),
            (5, 'Premium (+ Alarm System)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Security Features'
    )
    
    fire_safety = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Fire Safety Equipment Installed?'
    )


class VehicleCalculatorForm(forms.Form):
    vehicle_value = forms.IntegerField(
        min_value=100000,
        max_value=50000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 1500000'
        }),
        label='Vehicle Value (PKR)'
    )
    
    vehicle_type = forms.ChoiceField(
        choices=[
            ('car_800cc', 'Car (800cc - 1000cc)'),
            ('car_1300cc', 'Car (1300cc - 1600cc)'),
            ('car_1800cc', 'Car (1800cc - 2500cc)'),
            ('car_luxury', 'Car (Luxury 2500cc+)'),
            ('suv', 'SUV/Crossover'),
            ('bike_70cc', 'Motorcycle (70cc - 125cc)'),
            ('bike_heavy', 'Motorcycle (150cc+)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Vehicle Type'
    )
    
    vehicle_age = forms.IntegerField(
        min_value=0,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Age in years'
        }),
        label='Vehicle Age (Years)'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City of Registration'
    )
    
    driver_age = forms.IntegerField(
        min_value=18,
        max_value=80,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primary driver age'
        }),
        label='Driver Age (Years)'
    )
    
    driver_experience = forms.IntegerField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Years of driving'
        }),
        label='Driving Experience (Years)'
    )
    
    claims_history = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of claims'
        }),
        label='Previous Claims (Last 5 Years)'
    )


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Claim

# Existing calculator forms...
PAKISTANI_CITIES = [
    ('karachi', 'Karachi'),
    ('lahore', 'Lahore'),
    ('islamabad', 'Islamabad'),
    ('rawalpindi', 'Rawalpindi'),
    ('faisalabad', 'Faisalabad'),
    ('multan', 'Multan'),
    ('peshawar', 'Peshawar'),
    ('quetta', 'Quetta'),
    ('sialkot', 'Sialkot'),
    ('gujranwala', 'Gujranwala'),
]

# Authentication Forms
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '03XX-XXXXXXX'
        })
    )
    cnic = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXXX-XXXXXXX-X'
        }),
        label='CNIC Number'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Full Address',
            'rows': 3
        })
    )
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# Claim Form
class ClaimSubmissionForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_amount', 'incident_date', 'incident_description', 
                  'document1', 'document2', 'document3']
        widgets = {
            'claim_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter claim amount in PKR'
            }),
            'incident_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'incident_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the incident in detail...'
            }),
            'document1': forms.FileInput(attrs={'class': 'form-control'}),
            'document2': forms.FileInput(attrs={'class': 'form-control'}),
            'document3': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'document1': 'Supporting Document 1 (Medical Bills/Police Report)',
            'document2': 'Supporting Document 2 (Photos/Receipts)',
            'document3': 'Supporting Document 3 (Additional Evidence)',
        }


class ClaimReviewForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['status', 'approved_amount', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


# Payment Form
class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('stripe', 'Credit/Debit Card (Stripe)'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Payment Method'
    )
    
    # Stripe card details (will be handled by Stripe.js)
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'id': 'card-number'
        })
    )
    
    card_expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'id': 'card-expiry'
        })
    )
    
    card_cvc = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVC',
            'id': 'card-cvc'
        })
    )


# Keep all existing calculator forms (HealthCalculatorForm, etc.)
class HealthCalculatorForm(forms.Form):
    age = forms.IntegerField(
        min_value=18, 
        max_value=80,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        label='Age (Years)'
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    
    height = forms.FloatField(
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Height in cm',
            'step': '0.1'
        }),
        label='Height (cm)'
    )
    
    weight = forms.FloatField(
        min_value=30,
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Weight in kg',
            'step': '0.1'
        }),
        label='Weight (kg)'
    )
    
    smoker = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Are you a smoker?'
    )
    
    pre_existing_conditions = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of conditions'
        }),
        label='Pre-existing Medical Conditions (Count)'
    )
    
    coverage_amount = forms.IntegerField(
        min_value=100000,
        max_value=10000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 500000'
        }),
        label='Desired Coverage Amount (PKR)'
    )


class LifeCalculatorForm(forms.Form):
    age = forms.IntegerField(
        min_value=18,
        max_value=70,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        label='Age (Years)'
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Gender'
    )
    
    smoker = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Are you a smoker?'
    )
    
    occupation_risk = forms.ChoiceField(
        choices=[
            (1, 'Low Risk (Office Work)'),
            (2, 'Moderate Risk (Teaching, Sales)'),
            (3, 'Medium Risk (Driver, Factory Worker)'),
            (4, 'High Risk (Construction, Mining)'),
            (5, 'Very High Risk (Military, Police)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Occupation Risk Level'
    )
    
    coverage_amount = forms.IntegerField(
        min_value=500000,
        max_value=50000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 5000000'
        }),
        label='Sum Assured (PKR)'
    )
    
    policy_term = forms.IntegerField(
        min_value=5,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 20'
        }),
        label='Policy Term (Years)'
    )


class PropertyCalculatorForm(forms.Form):
    property_value = forms.IntegerField(
        min_value=1000000,
        max_value=500000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 10000000'
        }),
        label='Property Value (PKR)'
    )
    
    property_type = forms.ChoiceField(
        choices=[
            ('house', 'Residential House'),
            ('apartment', 'Apartment/Flat'),
            ('commercial', 'Commercial Building'),
            ('shop', 'Shop'),
            ('warehouse', 'Warehouse'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Property Type'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    
    construction_year = forms.IntegerField(
        min_value=1950,
        max_value=2024,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2015'
        }),
        label='Year of Construction'
    )
    
    security_features = forms.ChoiceField(
        choices=[
            (0, 'No Security'),
            (1, 'Basic (Locks only)'),
            (2, 'Standard (Locks + Grills)'),
            (3, 'Good (+ Security Guard)'),
            (4, 'Excellent (+ CCTV)'),
            (5, 'Premium (+ Alarm System)')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Security Features'
    )
    
    fire_safety = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Fire Safety Equipment Installed?'
    )


class VehicleCalculatorForm(forms.Form):
    vehicle_value = forms.IntegerField(
        min_value=100000,
        max_value=50000000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 1500000'
        }),
        label='Vehicle Value (PKR)'
    )
    
    vehicle_type = forms.ChoiceField(
        choices=[
            ('car_800cc', 'Car (800cc - 1000cc)'),
            ('car_1300cc', 'Car (1300cc - 1600cc)'),
            ('car_1800cc', 'Car (1800cc - 2500cc)'),
            ('car_luxury', 'Car (Luxury 2500cc+)'),
            ('suv', 'SUV/Crossover'),
            ('bike_70cc', 'Motorcycle (70cc - 125cc)'),
            ('bike_heavy', 'Motorcycle (150cc+)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Vehicle Type'
    )
    
    vehicle_age = forms.IntegerField(
        min_value=0,
        max_value=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Age in years'
        }),
        label='Vehicle Age (Years)'
    )
    
    city = forms.ChoiceField(
        choices=PAKISTANI_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City of Registration'
    )
    
    driver_age = forms.IntegerField(
        min_value=18,
        max_value=80,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primary driver age'
        }),
        label='Driver Age (Years)'
    )
    
    driver_experience = forms.IntegerField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Years of driving'
        }),
        label='Driving Experience (Years)'
    )
    
    claims_history = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of claims'
        }),
        label='Previous Claims (Last 5 Years)'
    )

 
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 p-2',
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control rounded-3 p-2',
                'placeholder': 'Enter your last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-3 p-2',
                'placeholder': 'Enter your email address',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control rounded-3 p-2',
                'placeholder': 'Enter your phone number',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select rounded-3 p-2',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-3 p-2',
                'rows': 4,
                'placeholder': 'Write your message...',
            }),
        }