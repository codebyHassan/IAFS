from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PremiumCalculation(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('property', 'Property Insurance'),
        ('vehicle', 'Vehicle Insurance'),
    ]
    
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    calculated_premium = models.DecimalField(max_digits=10, decimal_places=2)
    input_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.insurance_type} - PKR {self.calculated_premium}"


class HealthCalculation(models.Model):
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)])
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    bmi = models.FloatField()
    smoker = models.BooleanField(default=False)
    pre_existing_conditions = models.IntegerField(default=0)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Health - {self.age}y - PKR {self.premium}"


class LifeCalculation(models.Model):
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)])
    gender = models.CharField(max_length=10)
    smoker = models.BooleanField(default=False)
    occupation_risk = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    policy_term = models.IntegerField()
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Life - {self.age}y - PKR {self.premium}"


class PropertyCalculation(models.Model):
    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    construction_year = models.IntegerField()
    security_features = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    fire_safety = models.BooleanField(default=False)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Property - {self.property_type} - PKR {self.premium}"


class VehicleCalculation(models.Model):
    vehicle_value = models.DecimalField(max_digits=12, decimal_places=2)
    vehicle_type = models.CharField(max_length=50)
    vehicle_age = models.IntegerField()
    city = models.CharField(max_length=50)
    driver_age = models.IntegerField()
    driver_experience = models.IntegerField()
    claims_history = models.IntegerField(default=0)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vehicle - {self.vehicle_type} - PKR {self.premium}"
    

    from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    cnic = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Policy(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('property', 'Property Insurance'),
        ('vehicle', 'Vehicle Insurance'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    policy_number = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    
    # Premium Details
    monthly_premium = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_premium = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Policy Details
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Additional Data
    policy_data = models.JSONField()  # Store all input data
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Policies'
    
    def __str__(self):
        return f"{self.policy_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.policy_number:
            # Generate unique policy number
            prefix = self.insurance_type[:3].upper()
            random_part = str(uuid.uuid4().int)[:8]
            self.policy_number = f"{prefix}{random_part}"
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status == 'active' and self.end_date >= timezone.now().date()
    
    @property
    def days_remaining(self):
        if self.is_active:
            delta = self.end_date - timezone.now().date()
            return delta.days
        return 0


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD = [
        ('stripe', 'Stripe'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.transaction_id} - PKR {self.amount}"


class Claim(models.Model):
    CLAIM_STATUS = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('settled', 'Settled'),
    ]
    
    claim_number = models.CharField(max_length=20, unique=True, editable=False)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    incident_date = models.DateField()
    incident_description = models.TextField()
    
    # Documents
    document1 = models.FileField(upload_to='claim_documents/', blank=True, null=True)
    document2 = models.FileField(upload_to='claim_documents/', blank=True, null=True)
    document3 = models.FileField(upload_to='claim_documents/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='submitted')
    admin_notes = models.TextField(blank=True, null=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.claim_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.claim_number:
            # Generate unique claim number
            prefix = "CLM"
            random_part = str(uuid.uuid4().int)[:10]
            self.claim_number = f"{prefix}{random_part}"
        super().save(*args, **kwargs)


# Keep existing calculation models
class PremiumCalculation(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('property', 'Property Insurance'),
        ('vehicle', 'Vehicle Insurance'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    calculated_premium = models.DecimalField(max_digits=10, decimal_places=2)
    input_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.insurance_type} - PKR {self.calculated_premium}"


class HealthCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)])
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    bmi = models.FloatField()
    smoker = models.BooleanField(default=False)
    pre_existing_conditions = models.IntegerField(default=0)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Health - {self.age}y - PKR {self.premium}"


class LifeCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(70)])
    gender = models.CharField(max_length=10)
    smoker = models.BooleanField(default=False)
    occupation_risk = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    policy_term = models.IntegerField()
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Life - {self.age}y - PKR {self.premium}"


class PropertyCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    construction_year = models.IntegerField()
    security_features = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    fire_safety = models.BooleanField(default=False)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Property - {self.property_type} - PKR {self.premium}"


class VehicleCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_value = models.DecimalField(max_digits=12, decimal_places=2)
    vehicle_type = models.CharField(max_length=50)
    vehicle_age = models.IntegerField()
    city = models.CharField(max_length=50)
    driver_age = models.IntegerField()
    driver_experience = models.IntegerField()
    claims_history = models.IntegerField(default=0)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vehicle - {self.vehicle_type} - PKR {self.premium}"
    

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health Insurance'),
        ('vehicle', 'Vehicle Insurance'),
        ('life', 'Life Insurance'),
        ('property', 'Property Insurance'),
        ('tips', 'Tips & Guides'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_time = models.PositiveIntegerField(default=5)  # minutes

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('policy', 'Policy Inquiry'),
        ('claim', 'Claim Support'),
        ('payment', 'Payment Issue'),
        ('general', 'General Question'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
