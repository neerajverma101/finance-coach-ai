"""
Enhanced Dashboard with Plotly Charts and Recommendations
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dashboard - Finance Coach",
    page_icon="📊",
    layout="wide",
)

# Sidebar
with st.sidebar:
    st.title("💰 Finance AI Coach")
    st.markdown("---")
    st.markdown("### 📍 Pages")
    
    if st.button("📝 Get Started", use_container_width=True, key="nav_onboard"):
        st.switch_page("pages/1_onboarding.py")
    
    # Current page indicator
    st.button("📊 Dashboard", use_container_width=True, disabled=True, key="current_page")
    
    if st.button("🎯 Goals", use_container_width=True, key="nav_goals"):
        st.switch_page("pages/3_goals.py")

# Main content
st.title("📊 Your Financial Dashboard")

# Check if analysis exists
# Auto-calculate if data exists but analysis is missing (for returning guests)
# Auto-calculate if data exists but analysis is missing (for returning guests)
has_data = (st.session_state.guest_data.get('snapshot') or 
            st.session_state.guest_data.get('assets') or 
            st.session_state.guest_data.get('liabilities'))

if 'guest_data' in st.session_state and has_data and not st.session_state.guest_data.get('analysis'):
    from services.calculator import FinancialCalculator
    try:
        analysis = FinancialCalculator.analyze_financial_health(
            st.session_state.guest_data['snapshot'],
            st.session_state.guest_data['assets'],
            st.session_state.guest_data['liabilities']
        )
        st.session_state.guest_data['analysis'] = analysis
        st.rerun()
    except Exception as e:
        print(f"Auto-calc error: {e}")

if 'guest_data' not in st.session_state or not st.session_state.guest_data.get('analysis'):
    st.warning("⚠️ No analysis data available. Please complete the onboarding first!")
    if st.button("📝 Go to Onboarding"):
        st.switch_page("pages/1_onboarding.py")
else:
    analysis = st.session_state.guest_data['analysis']
    metrics = analysis['metrics']
    scores = analysis['scores']
    snapshot = st.session_state.guest_data['snapshot']
    
    # Key Metrics
    st.markdown("### 💰 Your Financial Snapshot")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if metrics['net_worth'] >= 0 else "inverse"
        st.metric(
            "Net Worth",
            f"₹{metrics['net_worth']:,.0f}",
            delta=f"{'Positive' if metrics['net_worth'] >= 0 else 'Negative'}",
            delta_color=delta_color
        )
    
    with col2:
        delta_color = "normal" if metrics['savings_rate'] >= 20 else "inverse"
        st.metric(
            "Savings Rate",
            f"{metrics['savings_rate']:.1f}%",
            delta="Healthy" if metrics['savings_rate'] >= 20 else "Needs Improvement",
            delta_color=delta_color
        )
    
    with col3:
        delta_color = "normal" if metrics['emergency_months'] >= 3 else "inverse"
        st.metric(
            "Emergency Fund",
            f"{metrics['emergency_months']:.1f} months",
            delta="Safe" if metrics['emergency_months'] >= 3 else "Build Up",
            delta_color=delta_color
        )
    
    with col4:
        delta_color = "normal" if metrics['monthly_surplus'] > 0 else "inverse"
        st.metric(
            "Monthly Surplus",
            f"₹{metrics['monthly_surplus']:,.0f}",
            delta="Saving" if metrics['monthly_surplus'] > 0 else "Deficit",
            delta_color=delta_color
        )
    
    # Charts Row 1
    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 📊 Income vs Expenses")
        
        # Income vs Expenses Bar Chart
        fig_income_expense = go.Figure()
        fig_income_expense.add_trace(go.Bar(
            name='Monthly',
            x=['Income', 'Expenses', 'Surplus'],
            y=[snapshot['monthly_income'], snapshot['monthly_expenses'], metrics['monthly_surplus']],
            marker_color=['#10b981', '#ef4444', '#6366f1']
        ))
        fig_income_expense.update_layout(
            height=300,
            showlegend=False,
            yaxis_title="Amount (₹)",
            template="plotly_white"
        )
        st.plotly_chart(fig_income_expense, use_container_width=True)
    
    with chart_col2:
        st.markdown("#### 💼 Assets vs Liabilities")
        
        # Assets vs Liabilities Pie Chart
        fig_assets_liab = go.Figure(data=[go.Pie(
            labels=['Assets', 'Liabilities'],
            values=[metrics['total_assets'], metrics['total_liabilities']],
            marker_colors=['#10b981', '#ef4444'],
            hole=0.4
        )])
        fig_assets_liab.update_layout(
            height=300,
            showlegend=True,
            template="plotly_white"
        )
        st.plotly_chart(fig_assets_liab, use_container_width=True)
    
    # Health Scores with Visual Gauge
    st.markdown("---")
    st.markdown("### 📈 Financial Health Scores")
    
    score_col1, score_col2, score_col3, score_col4 = st.columns(4)
    
    def create_gauge(value, title):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#6366f1"},
                'steps': [
                    {'range': [0, 33], 'color': "#fecaca"},
                    {'range': [33, 66], 'color': "#fde68a"},
                    {'range': [66, 100], 'color': "#bbf7d0"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        return fig
    
    with score_col1:
        st.plotly_chart(create_gauge(scores['emergency_fund'], "Emergency Fund"), use_container_width=True)
    
    with score_col2:
        st.plotly_chart(create_gauge(scores['savings'], "Savings Rate"), use_container_width=True)
    
    with score_col3:
        st.plotly_chart(create_gauge(scores['debt'], "Debt Health"), use_container_width=True)
    
    with score_col4:
        st.plotly_chart(create_gauge(scores['overall_health'], "Overall Health"), use_container_width=True)
    
    # Overall Health Summary
    st.markdown("---")
    if scores['overall_health'] >= 75:
        st.success(f"✅ **Excellent financial health!** Overall Score: **{scores['overall_health']:.0f}/100**")
        st.info("Keep up the great work! You're on track to achieve your financial goals.")
    elif scores['overall_health'] >= 50:
        st.info(f"💡 **Good progress!** Overall Score: **{scores['overall_health']:.0f}/100**")
        st.warning("A few improvements will boost your financial health significantly.")
    else:
        st.warning(f"⚠️ **Needs attention.** Overall Score: **{scores['overall_health']:.0f}/100**")
        st.error("Follow the recommendations below to improve your financial situation.")
    
    # Personalized Recommendations via Rule Engine
    st.markdown("---")
    st.markdown("### 🎯 Your Top 3 Priorities")
    
    from services.rule_service import RuleService, PriorityLevel
    
    # Get priorities from Rule Engine
    recommendations = RuleService.evaluate_priorities(
        st.session_state.guest_data['snapshot'],
        st.session_state.guest_data['liabilities']
    )
    
    if not recommendations:
        st.success("🎉 You have no critical financial issues! Great job!")
        st.info("Consider expanding your investments or saving for a major goal.")
        
    # Display recommendations
    for rec in recommendations[:3]:  # Top 3 only
        # Determine color based on priority
        emoji = "⚪"
        if rec.priority == PriorityLevel.CRITICAL:
            emoji = "🔴"
        elif rec.priority == PriorityLevel.HIGH:
            emoji = "🟠" 
        elif rec.priority == PriorityLevel.MEDIUM:
            emoji = "🟡"
        elif rec.priority == PriorityLevel.LOW:
            emoji = "🟢"
            
        with st.expander(f"**{emoji} {rec.title}**", expanded=True):
            st.markdown(f"**Situation:** {rec.description}")
            if rec.recommended_amount:
                st.markdown(f"**Target:** ₹{rec.recommended_amount:,.0f}")
                
            # Action button based on type
            if rec.action_type == 'save':
                if st.button("Set Savings Goal", key=f"act_{rec.rule_id}"):
                    st.session_state.guest_data['goals'].append({
                        'name': rec.title,
                        'target_amount': rec.recommended_amount or 0,
                        'current_progress': 0,
                        'category': 'Emergency',
                        'target_date': None
                    })
                    st.toast("Goal added! Go to Goals page to finalize.", icon="✅")

    # Smart Allocations (Bucket Engine)
    if 'metrics' in locals() and metrics['monthly_surplus'] > 0:
        st.markdown("---")
        
        from services.bucket_service import BucketService
        
        # 1. Get Recommended Framework
        suggested_framework_enum = RuleService.recommend_framework(metrics)
        suggested_framework_name = suggested_framework_enum.value
        
        st.markdown(f"### 🏺 Smart Allocations ({suggested_framework_name})")
        st.info(f"💡 Strategy: **{suggested_framework_name}** selected based on your profile.")
        
        # 2. Allocate using this framework
        allocations = BucketService.allocate_surplus(
            metrics['monthly_surplus'], 
            recommendations,
            framework=suggested_framework_name
        )
        
        if allocations:
            b_col1, b_col2 = st.columns([1, 1])
            
            with b_col1:
                # Allocation Pie Chart
                labels = [a.name for a in allocations]
                values = [a.amount for a in allocations]
                
                fig_bucket = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.5,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Pastel)
                )])
                fig_bucket.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                st.plotly_chart(fig_bucket, use_container_width=True)
            
            with b_col2:
                st.write(f"**Total Surplus: ₹{metrics['monthly_surplus']:,.0f}**")
                for alloc in allocations:
                    st.write(f"**{alloc.name}**: ₹{alloc.amount:,.0f} ({alloc.percentage}%)")
                    st.progress(alloc.percentage / 100)

    
    # Breakdown
    st.markdown("---")
    st.markdown("### 💼 Detailed Breakdown")
    
    breakdown_col1, breakdown_col2 = st.columns(2)
    
    with breakdown_col1:
        st.subheader(f"💰 Assets: ₹{metrics['total_assets']:,.0f}")
        if st.session_state.guest_data['assets']:
            for asset in st.session_state.guest_data['assets']:
                percentage = (asset['value'] / metrics['total_assets'] * 100) if metrics['total_assets'] > 0 else 0
                st.write(f"• **{asset['name']}**: ₹{asset['value']:,.0f} ({percentage:.1f}%)")
        else:
            st.caption("No assets added yet")
    
    with breakdown_col2:
        st.subheader(f"💳 Liabilities: ₹{metrics['total_liabilities']:,.0f}")
        if st.session_state.guest_data['liabilities']:
            for debt in st.session_state.guest_data['liabilities']:
                percentage = (debt['outstanding'] / metrics['total_liabilities'] * 100) if metrics['total_liabilities'] > 0 else 0
                st.write(f"• **{debt['name']}**: ₹{debt['outstanding']:,.0f} @ {debt['interest_rate']*100:.1f}% APR ({percentage:.1f}%)")
        else:
            st.caption("No liabilities - Great job!")
    
    # Link to Goals
    st.markdown("---")
    if st.button("🎯 Set Financial Goals Based on This Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/3_goals.py")
