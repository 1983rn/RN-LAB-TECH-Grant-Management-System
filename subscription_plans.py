"""
Standardized Subscription Plans Configuration
Single Source of Truth for all subscription plans
"""

SUBSCRIPTION_PLANS = {
    "trial": {
        "name": "Starter Trial Plan",
        "duration_days": 7,
        "price": 0.00
    },
    "term1": {
        "name": "Single Term Plan",
        "duration_days": 90,
        "price": 300000.00
    },
    "term2": {
        "name": "Two-Term Plan",
        "duration_days": 180,
        "price": 500000.00
    },
    "annual": {
        "name": "Annual Plan",
        "duration_days": 270,
        "price": 800000.00
    },
    "two_year": {
        "name": "Two-Year Institutional Plan",
        "duration_days": 540,
        "price": 1500000.00
    },
    "three_year": {
        "name": "Three-Year Strategic Plan",
        "duration_days": 810,
        "price": 2500000.00
    }
}

def get_plan(plan_key):
    """Get plan details by key"""
    return SUBSCRIPTION_PLANS.get(plan_key)

def get_all_plans():
    """Get all available plans"""
    return SUBSCRIPTION_PLANS
