import numpy as np
from datetime import datetime

class PropertyPremiumModel:
    def calculate_premium(self, property_value, property_type, city, 
                         construction_year, security_features, fire_safety):
        """Calculate property insurance premium"""
        
        # Base rate (annual premium as % of property value)
        base_rate = 0.004  # 0.4%
        
        # Property type factor
        type_factors = {
            'house': 1.0,
            'apartment': 0.9,
            'commercial': 1.3,
            'shop': 1.4,
            'warehouse': 1.5,
        }
        type_factor = type_factors.get(property_type, 1.0)
        
        # City risk factor (crime, natural disasters)
        city_factors = {
            'karachi': 1.3,  # High crime, coastal
            'lahore': 1.2,
            'islamabad': 0.9,  # Lowest risk
            'rawalpindi': 1.0,
            'faisalabad': 1.1,
            'multan': 1.15,
            'peshawar': 1.4,  # Security concerns
            'quetta': 1.5,  # Earthquake zone
            'sialkot': 1.0,
            'gujranwala': 1.1,
        }
        city_factor = city_factors.get(city, 1.1)
        
        # Building age factor
        current_year = datetime.now().year
        building_age = current_year - construction_year
        
        if building_age < 5:
            age_factor = 0.9
        elif building_age < 10:
            age_factor = 1.0
        elif building_age < 20:
            age_factor = 1.2
        elif building_age < 30:
            age_factor = 1.4
        else:
            age_factor = 1.7
        
        # Security features discount
        security_discount = 1 - (int(security_features) * 0.05)
        security_discount = max(security_discount, 0.75)  # Max 25% discount
        
        # Fire safety discount
        fire_discount = 0.9 if fire_safety else 1.0
        
        # Calculate annual premium
        annual_premium = (property_value * base_rate * type_factor * 
                         city_factor * age_factor * security_discount * 
                         fire_discount)
        
        monthly_premium = annual_premium / 12
        
        # Add randomness
        randomness = np.random.uniform(0.95, 1.05)
        monthly_premium *= randomness
        
        # Round to nearest 100
        monthly_premium = round(monthly_premium / 100) * 100
        
        # Minimum premium
        monthly_premium = max(monthly_premium, 3000)
        
        return {
            'monthly_premium': round(monthly_premium, 2),
            'yearly_premium': round(monthly_premium * 12, 2),
            'coverage_amount': round(property_value, 2),
            'building_age': building_age,
            'risk_level': self._calculate_risk_level(city, building_age, security_features)
        }
    
    def _calculate_risk_level(self, city, building_age, security_features):
        risk_score = 0
        
        high_risk_cities = ['karachi', 'peshawar', 'quetta']
        if city in high_risk_cities:
            risk_score += 3
        elif city in ['lahore', 'multan']:
            risk_score += 2
        else:
            risk_score += 1
        
        if building_age > 30:
            risk_score += 3
        elif building_age > 20:
            risk_score += 2
        elif building_age > 10:
            risk_score += 1
        
        risk_score -= int(security_features)
        
        if risk_score <= 2:
            return 'Low'
        elif risk_score <= 4:
            return 'Medium'
        else:
            return 'High'