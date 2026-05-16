from django.urls import path
from . import views

urlpatterns = [
    

    
    path('health-calculator/', views.health_calculator, name='health_calculator'),
    path('life-calculator/', views.life_calculator, name='life_calculator'),
    path('property-calculator/', views.property_calculator, name='property_calculator'),
    path('vehicle-calculator/', views.vehicle_calculator, name='vehicle_calculator'),
    path('result/', views.result, name='result'),
]

from django.urls import path
from . import views

urlpatterns = [
    # main nav links
    path('', views.index , name='index'),
    path('about/', views.about , name='about'), 
    path('contact/', views.contact_view, name='contact'),        # path('blog/', views.blog , name='blog'),  
    path('plans/', views.plans , name='plans'),  
        

    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),

    #preiume
    path('preiume/', views.home, name='home'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Calculators
    path('health-calculator/', views.health_calculator, name='health_calculator'),
    path('life-calculator/', views.life_calculator, name='life_calculator'),
    path('property-calculator/', views.property_calculator, name='property_calculator'),
    path('vehicle-calculator/', views.vehicle_calculator, name='vehicle_calculator'),
    path('result/', views.result, name='result'),
    
    # Policy Purchase
    path('buy-policy/', views.buy_policy, name='buy_policy'),
    path('payment/<int:policy_id>/', views.payment_page, name='payment_page'),
    path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('policy/<int:policy_id>/', views.policy_detail, name='policy_detail'),
    
    # Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my-policies/', views.my_policies, name='my_policies'),
    path('my-claims/', views.my_claims, name='my_claims'),
    
    # Claims
    path('submit-claim/<int:policy_id>/', views.submit_claim, name='submit_claim'),
    path('claim/<int:claim_id>/', views.claim_detail, name='claim_detail'),
    
    # Admin
    path('admin-claims/', views.admin_claims, name='admin_claims'),
    path('review-claim/<int:claim_id>/', views.review_claim, name='review_claim'),
]