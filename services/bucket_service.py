from typing import List, Dict, Any
from services.rule_service import FinancialAction, PriorityLevel

class BucketAllocation:
    def __init__(self, name: str, amount: float, percentage: float, priority: str):
        self.name = name
        self.amount = amount
        self.percentage = percentage
        self.priority = priority

class BucketService:
    """
    Allocates monthly surplus into financial buckets based on priorities.
    """
    
    @staticmethod
    def allocate_surplus(surplus: float, priorities: List[FinancialAction], framework: str = "50/30/20 Rule") -> List[BucketAllocation]:
        """
        Distribute surplus money into buckets based on Framework and Priorities.
        """
        if surplus <= 0:
            return []
            
        allocations = []
        
        # 1. CRITICAL PRIORITIES (Always Override)
        # If there's a critical need (Emergency/Debt), allocate 80-100% there first
        critical_priority = next((p for p in priorities if p.priority == PriorityLevel.CRITICAL), None)
        
        if critical_priority:
            allocations.append(BucketAllocation(critical_priority.title, surplus, 100, "Critical"))
            return allocations

        # 2. FRAMEWORK LOGIC (If no critical issues)
        
        if framework == "Debt Avalanche":
             # 90% to Debt, 10% Buffer
             allocations.append(BucketAllocation("Debt Payoff", surplus * 0.9, 90, "Debt"))
             allocations.append(BucketAllocation("Buffer", surplus * 0.1, 10, "Safety"))
             
        elif framework == "6 Jars System":
            # Modified for Surplus Only (since Needs are paid)
            # FFA (10%), Long-term (10%), Play (10%), Edu (10%), Give (5%), Savings (remaining)
            # Adjusting to surplus context:
            allocations.append(BucketAllocation("Financial Freedom (FFA)", surplus * 0.50, 50, "Invest"))
            allocations.append(BucketAllocation("Play / Fun", surplus * 0.10, 10, "Lifestyle"))
            allocations.append(BucketAllocation("Education", surplus * 0.10, 10, "Growth"))
            allocations.append(BucketAllocation("Long-term Savings", surplus * 0.20, 20, "Save"))
            allocations.append(BucketAllocation("Charity", surplus * 0.10, 10, "Give"))

        elif framework == "FIRE (Aggressive)":
            # 90% Invest, 10% Fun
            allocations.append(BucketAllocation("Aggressive Investing", surplus * 0.9, 90, "Invest"))
            allocations.append(BucketAllocation("Guilt-free Play", surplus * 0.1, 10, "Lifestyle"))
            
        else: # Default: 50/30/20 (Applied to Surplus)
            # Usually 50/30/20 applies to *Total Income*.
            # For Surplus, we assume "Needs" are covered.
            # So surplus splits into: 50% Savings/Invest, 30% Wants (Fun), 20% Buffer/Extra Debt
            allocations.append(BucketAllocation("Investments & Savings", surplus * 0.5, 50, "Future"))
            allocations.append(BucketAllocation("Wants / Goals", surplus * 0.3, 30, "Lifestyle"))
            allocations.append(BucketAllocation("Buffer / Extra", surplus * 0.2, 20, "Safety"))
            
        return allocations
