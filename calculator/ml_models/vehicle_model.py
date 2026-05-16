import numpy as np

class VehiclePremiumModel:
    def calculate_premium(self, vehicle_value, vehicle_type, vehicle_age, 
                         city, driver_age, driver_experience, claims_history):
        """Calculate vehicle insurance premium"""
        
        # Base rate (annual premium as % of vehicle value)
        base_rate = 0.05  # 5%
        
        # Vehicle type factor
        type_factors = {
            'car_800cc': 1.0,
            'car_1300cc': 1.2,
            'car_1800cc': 1.4,
            'car_luxury': 1.8,
            'suv': 1.5,
            'bike_70cc': 0.8,
            'bike_heavy': 1.3,
        }
        type_factor = type_factors.get(vehicle_type, 1.0)
        
        # Vehicle age depreciation
        if vehicle_age == 0:
            age_factor = 1.2  # New car, higher premium
        elif vehicle_age <= 3:
            age_factor = 1.0
        elif vehicle_age <= 7:
            age_factor = 0.85
        elif vehicle_age <= 10:
            age_factor = 0.7
        else:
            age_factor = 0.6
        
        # City risk factor (traffic, theft rates)
        city_factors = {
            'karachi': 1.4,  # Highest theft/accident rate
            'lahore': 1.3,
            'islamabad': 1.0,
            'rawalpindi': 1.15,
            'faisalabad': 1.2,
            'multan': 1.15,
            'peshawar': 1.35,
            'quetta': 1.25,
            'sialkot': 1.1,
            'gujranwala': 1.2,
        }
        city_factor = city_factors.get(city, 1.2)
        
        # Driver age factor
        if driver_age < 25:
            driver_age_factor = 1.5  # Young drivers
        elif driver_age < 30:
            driver_age_factor = 1.2
        elif driver_age < 60:
            driver_age_factor = 1.0
        else:
            driver_age_factor = 1.3  # Senior drivers
        
        # Driver experience discount
        if driver_experience >= 10:
            experience_discount = 0.85
        elif driver_experience >= 5:
            experience_discount = 0.9
        elif driver_experience >= 2:
            experience_discount = 0.95
        else:
            experience_discount = 1.0
        
        # Claims history penalty
        claims_penalty = 1 + (claims_history * 0.2)
        
        # Calculate annual premium
        annual_premium = (vehicle_value * base_rate * type_factor * 
                         age_factor * city_factor * driver_age_factor * 
                         experience_discount * claims_penalty)
        
        monthly_premium = annual_premium / 12
        
        # Add randomness
        randomness = np.random.uniform(0.95, 1.05)
        monthly_premium *= randomness
        
        # Round to nearest 100
        monthly_premium = round(monthly_premium / 100) * 100
        
        # Minimum premium
        monthly_premium = max(monthly_premium, 2000)
        
        # Calculate IDV (Insured Declared Value) with depreciation
        depreciation_rate = min(vehicle_age * 0.05, 0.5)  # Max 50% depreciation
        idv = vehicle_value * (1 - depreciation_rate)
        
        return {
            'monthly_premium': round(monthly_premium, 2),
            'yearly_premium': round(monthly_premium * 12, 2),
            'idv': round(idv, 2),
            'depreciation': round(depreciation_rate * 100, 1),
            'risk_level': self._calculate_risk_level(driver_age, driver_experience, claims_history)
        }
    
    def _calculate_risk_level(self, driver_age, driver_experience, claims_history):
        risk_score = 0
        
        if driver_age < 25 or driver_age > 65:
            risk_score += 3
        elif driver_age < 30:
            risk_score += 1
        
        if driver_experience < 2:
            risk_score += 3
        elif driver_experience < 5:
            risk_score += 1
        
        risk_score += claims_history * 2
        
        if risk_score <= 2:
            return 'Low'
        elif risk_score <= 5:
            return 'Medium'
        else:
            return 'High'