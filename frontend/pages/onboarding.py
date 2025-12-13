"""
Onboarding page - Simple financial data collection.
"""
import streamlit as st


def show():
    """Display onboarding form."""
    
    st.markdown("### Step 1: Financial Snapshot")
    st.markdown("Tell us about your monthly finances. Be as accurate as possible for better recommendations.")
    
    with st.form("snapshot_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_income = st.number_input(
                "💵 Monthly Income (₹)",
                min_value=0,
                value=st.session_state.guest_data['snapshot'].get('monthly_income', 0),
                step=1000,
                help="Your total monthly income after taxes"
            )
            
            current_savings = st.number_input(
                "💰 Current Savings (₹)",
                min_value=0,
                value=st.session_state.guest_data['snapshot'].get('current_savings', 0),
                step=5000,
                help="Money you have in savings accounts, FDs, etc."
            )
        
        with col2:
            monthly_expenses = st.number_input(
                "💸 Monthly Expenses (₹)",
                min_value=0,
                value=st.session_state.guest_data['snapshot'].get('monthly_expenses', 0),
                step=1000,
                help="Your total monthly spending"
            )
        
        # Optional expense breakdown
        with st.expander("📊 Detailed Expense Breakdown (Optional)"):
            exp_col1, exp_col2, exp_col3 = st.columns(3)
            
            with exp_col1:
                rent = st.number_input("🏠 Rent", min_value=0, step=1000)
                groceries = st.number_input("🛒 Groceries", min_value=0, step=500)
                utilities = st.number_input("💡 Utilities", min_value=0, step=500)
            
            with exp_col2:
                transport = st.number_input("🚗 Transport", min_value=0, step=500)
                entertainment = st.number_input("🎬 Entertainment", min_value=0, step=500)
                healthcare = st.number_input("🏥 Healthcare", min_value=0, step=500)
            
            with exp_col3:
                education = st.number_input("📚 Education", min_value=0, step=1000)
                insurance = st.number_input("🛡️ Insurance", min_value=0, step=500)
                other = st.number_input("📦 Other", min_value=0, step=500)
        
        submitted = st.form_submit_button("➡️ Next: Assets & Debts", use_container_width=True)
        
        if submitted:
            # Validate
            if monthly_income == 0:
                st.error("Please enter your monthly income")
                return
            
            # Save to session
            st.session_state.guest_data['snapshot'] = {
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'current_savings': current_savings,
                'expense_breakdown': {
                    'rent': rent,
                    'groceries': groceries,
                    'utilities': utilities,
                    'transport': transport,
                    'entertainment': entertainment,
                    'healthcare': healthcare,
                    'education': education,
                    'insurance': insurance,
                    'other': other
                } if rent > 0 or groceries > 0 else None
            }
            
            st.success("✅ Snapshot saved!")
            st.session_state.onboarding_step = 2
            st.rerun()
    
    # Step 2: Assets & Liabilities
    if st.session_state.get('onboarding_step', 1) >= 2:
        st.markdown("---")
        st.markdown("### Step 2: Assets & Debts")
        
        tab1, tab2 = st.tabs(["💰 Assets", "💳 Debts"])
        
        with tab1:
            st.markdown("Add your investments and assets")
            
            with st.form("asset_form"):
                asset_type = st.selectbox(
                    "Type",
                    ["Cash", "Fixed Deposit", "Mutual Fund", "Stocks", "Gold", "Other"]
                )
                asset_name = st.text_input("Name", placeholder="e.g., HDFC Equity Fund")
                asset_value = st.number_input("Current Value (₹)", min_value=0, step=1000)
                
                if st.form_submit_button("➕ Add Asset"):
                    if asset_name and asset_value > 0:
                        st.session_state.guest_data['assets'].append({
                            'type': asset_type.lower().replace(' ', '_'),
                            'name': asset_name,
                            'value': asset_value
                        })
                        st.success(f"✅ Added {asset_name}")
                        st.rerun()
            
            # Show existing assets
            if st.session_state.guest_data['assets']:
                st.markdown("**Your Assets:**")
                total_assets = sum(a['value'] for a in st.session_state.guest_data['assets'])
                
                for idx, asset in enumerate(st.session_state.guest_data['assets']):
                    col1, col2, col3 = st.columns([3, 2, 1])
                    col1.write(f"**{asset['name']}**")
                    col2.write(f"₹{asset['value']:,.0f}")
                    if col3.button("🗑️", key=f"del_asset_{idx}"):
                        st.session_state.guest_data['assets'].pop(idx)
                        st.rerun()
                
                st.metric("Total Assets", f"₹{total_assets:,.0f}")
        
        with tab2:
            st.markdown("Add your loans and credit card debt")
            
            with st.form("liability_form"):
                debt_type = st.selectbox(
                    "Type",
                    ["Credit Card", "Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Other"]
                )
                debt_name = st.text_input("Name", placeholder="e.g., HDFC Credit Card")
                outstanding = st.number_input("Outstanding Amount (₹)", min_value=0, step=1000)
                interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=1.0, value=12.0)
                
                if st.form_submit_button("➕ Add Debt"):
                    if debt_name and outstanding > 0:
                        st.session_state.guest_data['liabilities'].append({
                            'type': debt_type.lower().replace(' ', '_'),
                            'name': debt_name,
                            'outstanding': outstanding,
                            'interest_rate': interest_rate / 100  # Convert to decimal
                        })
                        
                        # Warning for high interest
                        if interest_rate > 15:
                            st.warning(f"⚠️ High interest rate! This should be a priority to pay off.")
                        
                        st.success(f"✅ Added {debt_name}")
                        st.rerun()
            
            # Show existing debts
            if st.session_state.guest_data['liabilities']:
                st.markdown("**Your Debts:**")
                total_debt = sum(l['outstanding'] for l in st.session_state.guest_data['liabilities'])
                
                for idx, debt in enumerate(st.session_state.guest_data['liabilities']):
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    col1.write(f"**{debt['name']}**")
                    col2.write(f"₹{debt['outstanding']:,.0f}")
                    col3.write(f"{debt['interest_rate']*100:.1f}% APR")
                    if col4.button("🗑️", key=f"del_debt_{idx}"):
                        st.session_state.guest_data['liabilities'].pop(idx)
                        st.rerun()
                
                st.metric("Total Debt", f"₹{total_debt:,.0f}", delta=None, delta_color="inverse")
        
        # Continue button
        st.markdown("---")
        if st.button("📊 Generate My Financial Analysis", use_container_width=True, type="primary"):
            # Calculate basic metrics and generate plan
            calculate_and_generate_plan()
            st.success("✅ Analysis complete! Check 'My Analysis' page.")
            st.balloons()


def calculate_and_generate_plan():
    """Calculate financial metrics and generate simple plan."""
    snapshot = st.session_state.guest_data['snapshot']
    assets = st.session_state.guest_data['assets']
    liabilities = st.session_state.guest_data['liabilities']
    
    # Calculate metrics
    total_assets = sum(a['value'] for a in assets) + snapshot.get('current_savings', 0)
    total_liabilities = sum(l['outstanding'] for l in liabilities)
    net_worth = total_assets - total_liabilities
    
    monthly_income = snapshot['monthly_income']
    monthly_expenses = snapshot['monthly_expenses']
    monthly_surplus = monthly_income - monthly_expenses
    
    savings_rate = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
    emergency_months = (snapshot.get('current_savings', 0) / monthly_expenses) if monthly_expenses > 0 else 0
    
    # Identify priorities
    priorities = []
    
    # Check emergency fund
    if emergency_months < 3:
        priorities.append({
            'order': 1,
            'title': 'Build Emergency Fund',
            'description': f'You have {emergency_months:.1f} months of expenses saved. Target: 3-6 months.',
            'impact': 'Financial security buffer',
            'monthly_allocation': min(monthly_surplus * 0.4, 5000)
        })
    
    # Check high-interest debt
    high_interest_debts = [l for l in liabilities if l['interest_rate'] > 0.12]
    if high_interest_debts:
        total_high_interest = sum(d['outstanding'] for d in high_interest_debts)
        avg_rate = sum(d['interest_rate'] for d in high_interest_debts) / len(high_interest_debts)
        
        priorities.append({
            'order': len(priorities) + 1,
            'title': 'Pay Off High-Interest Debt',
            'description': f'₹{total_high_interest:,.0f} at {avg_rate*100:.1f}% average interest rate.',
            'impact': f'Save ₹{total_high_interest * avg_rate / 12:,.0f}/month in interest',
            'monthly_allocation': min(monthly_surplus * 0.5, 15000)
        })
    
    # Investment allocation
    if savings_rate > 20 and emergency_months >= 3:
        priorities.append({
            'order': len(priorities) + 1,
            'title': 'Start/Continue Investing',
            'description': 'Build long-term wealth through systematic investing.',
            'impact': 'Projected wealth growth',
            'monthly_allocation': min(monthly_surplus * 0.3, 10000)
        })
    
    # Save plan
    st.session_state.guest_data['plan'] = {
        'metrics': {
            'net_worth': net_worth,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'savings_rate': savings_rate,
            'emergency_months': emergency_months,
            'monthly_surplus': monthly_surplus
        },
        'priorities': priorities[:3],  # Top 3
        'generated_at': st.session_state.guest_data.get('plan', {}).get('generated_at', None) or 'now'
    }
