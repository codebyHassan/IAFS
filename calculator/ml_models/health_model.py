import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class HealthPremiumModel:
    def __init__(self):
        self.model = None
        self.city_encoder = LabelEncoder()
        self.gender_encoder = LabelEncoder()
        self.model_path = os.path.join(
            os.path.dirname(__file__), 
            'trained_models', 
            'health_premium_model.pkl'
        )
    
    def calculate_bmi(self, height_cm, weight_kg):
        """Calculate BMI from height (cm) and weight (kg)"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def calculate_premium(self, age, gender, city, height, weight, smoker, 
                         pre_existing_conditions, coverage_amount):
        """Calculate health insurance premium"""
        
        # Calculate BMI
        bmi = self.calculate_bmi(height, weight)
        
        # Base premium calculation
        base_rate = 0.03  # 3% of coverage
        base_premium = coverage_amount * base_rate
        
        # Age factor
        if age < 25:
            age_factor = 0.8
        elif age < 35:
            age_factor = 1.0
        elif age < 45:
            age_factor = 1.3
        elif age < 55:
            age_factor = 1.7
        elif age < 65:
            age_factor = 2.2
        else:
            age_factor = 3.0
        
        # Gender factor (females generally have lower premiums)
        gender_factor = 1.0 if gender == 'male' else 0.9
        
        # BMI factor
        if bmi < 18.5:
            bmi_factor = 1.2  # Underweight
        elif 18.5 <= bmi < 25:
            bmi_factor = 1.0  # Normal
        elif 25 <= bmi < 30:
            bmi_factor = 1.3  # Overweight
        else:
            bmi_factor = 1.7  # Obese
        
        # Smoker factor
        smoker_factor = 1.5 if smoker else 1.0
        
        # Pre-existing conditions factor
        condition_factor = 1.0 + (pre_existing_conditions * 0.15)
        
        # City risk factor (higher crime/pollution = higher premium)
        city_factors = {
            'karachi': 1.2,
            'lahore': 1.15,
            'islamabad': 1.0,
            'rawalpindi': 1.05,
            'faisalabad': 1.1,
            'multan': 1.1,
            'peshawar': 1.25,
            'quetta': 1.3,
            'sialkot': 1.05,
            'gujranwala': 1.1,
        }
        city_factor = city_factors.get(city, 1.1)
        
        # Calculate monthly premium
        monthly_premium = (base_premium / 12) * age_factor * gender_factor * \
                         bmi_factor * smoker_factor * condition_factor * city_factor
        
        # Add some randomness for realism (±5%)
        randomness = np.random.uniform(0.95, 1.05)
        monthly_premium *= randomness
        
        # Round to nearest 100
        monthly_premium = round(monthly_premium / 100) * 100
        
        # Ensure minimum premium
        monthly_premium = max(monthly_premium, 2000)
        
        return {
            'monthly_premium': round(monthly_premium, 2),
            'yearly_premium': round(monthly_premium * 12, 2),
            'bmi': round(bmi, 2),
            'bmi_category': self._get_bmi_category(bmi),
            'risk_level': self._calculate_risk_level(age, bmi, smoker, pre_existing_conditions)
        }
    
    def _get_bmi_category(self, bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi < 25:
            return 'Normal'
        elif 25 <= bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    def _calculate_risk_level(self, age, bmi, smoker, conditions):
        risk_score = 0
        
        if age > 55:
            risk_score += 3
        elif age > 45:
            risk_score += 2
        elif age > 35:
            risk_score += 1
        
        if bmi < 18.5 or bmi > 30:
            risk_score += 2
        elif bmi > 25:
            risk_score += 1
        
        if smoker:
            risk_score += 3
        
        risk_score += conditions
        
        if risk_score <= 2:
            return 'Low'
        elif risk_score <= 5:
            return 'Medium'
        else:
            return 'High'