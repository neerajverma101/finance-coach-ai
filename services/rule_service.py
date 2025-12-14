from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel

class PriorityLevel(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    OPTIONAL = 5

class FrameworkType(Enum):
    FIFTY_THIRTY_TWENTY = "50/30/20 Rule"
    SIX_JARS = "6 Jars System"
    DEBT_AVALANCHE = "Debt Avalanche"
    FIRE_AGGRESSIVE = "FIRE (Aggressive)"

class FinancialAction(BaseModel):
    rule_id: str
    title: str
    description: str
    priority: PriorityLevel
    recommended_amount: Optional[float] = None
    action_type: str # 'save', 'pay_debt', 'invest'

class RuleService:
    """
    Deterministic Rule Engine for Personal Finance.
    Version: 1.0.0
    """
    
    @staticmethod
    def recommend_framework(metrics: Dict[str, Any]) -> FrameworkType:
        """
        Recommend a saving framework based on financial health.
        """
        # 1. High Debt -> Avalanche
        if metrics.get('total_liabilities', 0) > 0 and metrics.get('debt_to_income', 0) > 0.4:
            return FrameworkType.DEBT_AVALANCHE
            
        # 2. Aggressive Saver/High Income -> FIRE
        if metrics.get('savings_rate', 0) > 40:
             return FrameworkType.FIRE_AGGRESSIVE
             
        # 3. Healthy but needs structure -> 6 Jars
        if metrics.get('monthly_surplus', 0) > 50000 and metrics.get('overall_health', 0) > 70:
            return FrameworkType.SIX_JARS
            
        # 4. Default -> 50/30/20 (Good baseline)
        return FrameworkType.FIFTY_THIRTY_TWENTY

    @staticmethod
    def evaluate_priorities(snapshot: Dict[str, Any], liabilities: List[Dict[str, Any]]) -> List[FinancialAction]:
        """
        Evaluate financial health and return prioritized actions.
        
        Rules:
        1. Emergency Fund < 3 months expenses -> CRITICAL
        2. High Interest Debt (> 15%) -> CRITICAL
        3. Emergency Fund < 6 months -> HIGH
        4. Medium Interest Debt (> 8%) -> HIGH
        5. Savings Rate < 20% -> MEDIUM
        """
        priorities = []
        
        # Safe extraction of basic numbers
        monthly_income = float(snapshot.get('monthly_income', 0) or 0)
        monthly_expenses = float(snapshot.get('monthly_expenses', 0) or 0)
        current_savings = float(snapshot.get('current_savings', 0) or 0)
        monthly_surplus = monthly_income - monthly_expenses
        
        # --- Rule 1: Emergency Fund (Critical) ---
        required_emergency_fund = monthly_expenses * 3
        if current_savings < required_emergency_fund:
            shortfall = required_emergency_fund - current_savings
            priorities.append(FinancialAction(
                rule_id="RULE_EMERGENCY_CRITICAL",
                title="🚨 Build Emergency Fund (Critical)",
                description=f"You need ₹{shortfall:,.0f} more to reach 3 months of expenses. This is your safety net.",
                priority=PriorityLevel.CRITICAL,
                recommended_amount=shortfall,
                action_type="save"
            ))

        # --- Rule 2: High Interest Debt (Critical) ---
        for debt in liabilities:
            # Handle float/int conversion safely
            rate = float(debt.get('interest_rate', 0) or 0)
            # Normalize interest rate (e.g. 18.0 vs 0.18)
            if rate > 1:
                rate = rate / 100.0
                
            if rate > 0.15: # 15% threshold
                outstanding = float(debt.get('outstanding', 0) or 0)
                priorities.append(FinancialAction(
                    rule_id=f"RULE_DEBT_HIGH_{debt.get('name')}",
                    title=f"💳 Pay Off {debt.get('name')}",
                    description=f"Interest rate is {rate*100:.1f}%. This is wealth-destroying debt.",
                    priority=PriorityLevel.CRITICAL,
                    recommended_amount=outstanding,
                    action_type="pay_debt"
                ))

        # --- Rule 3: Emergency Fund (Comfort) ---
        # Only if Critical rule didn't trigger
        if current_savings >= required_emergency_fund:
            comfort_emergency_fund = monthly_expenses * 6
            if current_savings < comfort_emergency_fund:
                shortfall = comfort_emergency_fund - current_savings
                priorities.append(FinancialAction(
                    rule_id="RULE_EMERGENCY_COMFORT",
                    title="🛡️ Expand Emergency Fund",
                    description=f"Build up to 6 months of expenses (₹{comfort_emergency_fund:,.0f}) for extra security.",
                    priority=PriorityLevel.HIGH,
                    recommended_amount=shortfall,
                    action_type="save"
                ))

        # --- Rule 4: Savings Rate ---
        if monthly_income > 0:
            savings_rate = (monthly_surplus / monthly_income) * 100
            if savings_rate < 20:
                priorities.append(FinancialAction(
                    rule_id="RULE_SAVINGS_RATE",
                    title="📊 Improve Savings Rate",
                    description=f"Current rate: {savings_rate:.1f}%. Target: 20%. Try to cut discretionary spending.",
                    priority=PriorityLevel.MEDIUM,
                    action_type="analyze"
                ))
        
        # --- Rule 5: Investment (Growth) ---
        # If no critical priorities, suggest investing
        critical_issues = any(p.priority == PriorityLevel.CRITICAL for p in priorities)
        if not critical_issues and monthly_surplus > 0:
            priorities.append(FinancialAction(
                rule_id="RULE_INVEST_GROWTH",
                title="🚀 Invest for Growth",
                description="Your foundation is solid. Start investing in index funds or mutual funds.",
                priority=PriorityLevel.LOW,
                recommended_amount=monthly_surplus * 0.5,
                action_type="invest"
            ))

        # Sort by priority (CRITICAL=1 first)
        priorities.sort(key=lambda x: x.priority.value)
        return priorities
