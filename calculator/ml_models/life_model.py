import numpy as np

class LifePremiumModel:
    def calculate_premium(self, age, gender, smoker, occupation_risk, 
                         coverage_amount, policy_term):
        """Calculate life insurance premium"""
        
        # Base mortality rate (per 1000)
        base_mortality_rate = 0.002
        
        # Age factor (mortality increases with age)
        age_multiplier = 1 + ((age - 18) * 0.03)
        
        # Gender factor (males have higher mortality)
        gender_multiplier = 1.15 if gender == 'male' else 1.0
        
        # Smoking factor
        smoker_multiplier = 1.8 if smoker else 1.0
        
        # Occupation risk multiplier
        occupation_multiplier = 1 + (int(occupation_risk) * 0.2)
        
        # Policy term factor (longer term = slightly lower rate)
        term_discount = 1 - (policy_term * 0.005)
        term_discount = max(term_discount, 0.85)  # Max 15% discount
        
        # Calculate annual premium
        total_multiplier = (age_multiplier * gender_multiplier * 
                          smoker_multiplier * occupation_multiplier * 
                          term_discount)
        
        annual_premium = coverage_amount * base_mortality_rate * total_multiplier
        
        # Add administrative costs (10-15% of premium)
        admin_factor = 1.125
        annual_premium *= admin_factor
        
        monthly_premium = annual_premium / 12
        
        # Add randomness
        randomness = np.random.uniform(0.95, 1.05)
        monthly_premium *= randomness
        
        # Round to nearest 100
        monthly_premium = round(monthly_premium / 100) * 100
        
        # Minimum premium
        monthly_premium = max(monthly_premium, 1500)
        
        # Calculate maturity benefit (for endowment plans)
        maturity_benefit = coverage_amount * 0.6  # 60% of sum assured
        
        return {
            'monthly_premium': round(monthly_premium, 2),
            'yearly_premium': round(monthly_premium * 12, 2),
            'total_payable': round(monthly_premium * 12 * policy_term, 2),
            'maturity_benefit': round(maturity_benefit, 2),
            'risk_level': self._calculate_risk_level(age, smoker, occupation_risk)
        }
    
    def _calculate_risk_level(self, age, smoker, occupation_risk):
        risk_score = 0
        
        if age > 60:
            risk_score += 3
        elif age > 50:
            risk_score += 2
        elif age > 40:
            risk_score += 1
        
        if smoker:
            risk_score += 3
        
        risk_score += int(occupation_risk)
        
        if risk_score <= 3:
            return 'Low'
        elif risk_score <= 6:
            return 'Medium'
        else:
            return 'High'