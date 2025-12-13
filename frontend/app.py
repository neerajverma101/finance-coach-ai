"""
Streamlit application entry point for Personal Finance Coach.

Guest mode supported - no login required to test features.
Login only needed to save/retrieve data.
"""
import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Personal Finance Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/finance-coach',
        'Report a bug': 'https://github.com/yourusername/finance-coach/issues',
        'About': 'Personal Finance Coach - Your path to financial freedom'
    }
)

# Initialize session state for guest mode
if 'mode' not in st.session_state:
    st.session_state.mode = 'guest'  # 'guest' or 'logged_in'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Guest mode data storage (in session)
if 'guest_data' not in st.session_state:
    st.session_state.guest_data = {
        'profile': {},
        'snapshot': {},
        'assets': [],
        'liabilities': [],
        'goals': [],
        'plan': None
    }

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-light: #f8fafc;
        --text-dark: #1e293b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom headers */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Feature box */
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
    
    /* Guest mode badge */
    .guest-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: 600;
        display: inline-block;
        margin: 1rem 0;
    }
    
    /* CTA button */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 💰 Personal Finance Coach")
    
    # Show mode badge
    if st.session_state.mode == 'guest':
        st.markdown('<div class="guest-badge">🌟 Guest Mode</div>', unsafe_allow_html=True)
        st.info("💡 **Tip**: Login to save your progress!")
    else:
        st.success(f"✅ Logged in as: {st.session_state.user_email}")
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📝 Get Started", "📊 My Analysis", "🎯 Goals", "💾 Save Progress"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats (if data exists)
    if st.session_state.guest_data['snapshot']:
        st.markdown("### Quick Stats")
        income = st.session_state.guest_data['snapshot'].get('monthly_income', 0)
        expenses = st.session_state.guest_data['snapshot'].get('monthly_expenses', 0)
        
        if income > 0:
            savings_rate = ((income - expenses) / income * 100) if income > 0 else 0
            st.metric("Monthly Surplus", f"₹{income - expenses:,.0f}")
            st.metric("Savings Rate", f"{savings_rate:.1f}%")

# Main content based on navigation
if page == "🏠 Home":
    # Landing page
    st.markdown('<h1 class="main-header">Welcome to Personal Finance Coach</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your path to financial freedom starts here. No signup required to try!</p>', unsafe_allow_html=True)
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2>🎯 What We Do</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #475569;">
                We analyze your financial health, identify problems, organize your money into smart buckets, 
                and create a personalized action plan to help you achieve financial freedom.
            </p>
            <ul style="font-size: 1rem; color: #64748b; line-height: 2;">
                <li>✅ <strong>Understand</strong> your complete financial picture</li>
                <li>✅ <strong>Fix</strong> debt problems and build emergency funds</li>
                <li>✅ <strong>Organize</strong> money into clear buckets</li>
                <li>✅ <strong>Track</strong> progress with simple monthly check-ins</li>
                <li>✅ <strong>Learn</strong> with AI-powered explanations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Free Analysis", key="start_btn", use_container_width=True):
            st.session_state.page = "📝 Get Started"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🌟 Guest Mode</h3>
            <p>Try all features without creating an account!</p>
            <br>
            <p style="font-size: 0.9rem;">
                ✨ No email required<br>
                ✨ Full feature access<br>
                ✨ Save later if you like it
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>📊 Privacy First</h4>
            <p style="font-size: 0.9rem; color: #64748b;">
                Your data stays with you. We use self-reported information and 
                deterministic calculations - no bank access needed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("---")
    st.markdown("## 🛣️ How It Works")
    
    steps_cols = st.columns(4)
    
    with steps_cols[0]:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h1 style="color: #6366f1;">1️⃣</h1>
            <h4>Share Your Finances</h4>
            <p style="color: #64748b;">Income, expenses, assets, debts, goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_cols[1]:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h1 style="color: #8b5cf6;">2️⃣</h1>
            <h4>Get Analysis</h4>
            <p style="color: #64748b;">Net worth, debt health, savings rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_cols[2]:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h1 style="color: #ec4899;">3️⃣</h1>
            <h4>Receive Plan</h4>
            <p style="color: #64748b;">Top 3 actions + monthly targets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_cols[3]:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h1 style="color: #10b981;">4️⃣</h1>
            <h4>Track Progress</h4>
            <p style="color: #64748b;">Monthly check-ins + nudges</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features
    st.markdown("---")
    st.markdown("## ✨ Key Features")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        ### 🧮 Smart Analysis
        - Net worth calculation
        - Debt-to-income ratio
        - Emergency fund status
        - Savings rate tracking
        """)
    
    with feat_col2:
        st.markdown("""
        ### 🪣 Bucket System
        - Emergency fund bucket
        - Debt payoff bucket
        - Short-term goals
        - Long-term wealth
        """)
    
    with feat_col3:
        st.markdown("""
        ### 🤖 AI Assistant
        - "Why this?" explanations
        - Financial Q&A
        - Cited sources
        - Plain language
        """)

elif page == "📝 Get Started":
    st.title("📝 Let's Analyze Your Finances")
    st.markdown("Answer a few quick questions. Everything is **private** and stored only on your device (in guest mode).")
    
    # Import the onboarding page
    from pages import onboarding
    onboarding.show()

elif page == "📊 My Analysis":
    st.title("📊 Your Financial Analysis")
    
    # Check if user has entered data
    if not st.session_state.guest_data['snapshot']:
        st.warning("👈 Please complete the 'Get Started' section first!")
        if st.button("Go to Get Started"):
            st.session_state.page = "📝 Get Started"
            st.rerun()
    else:
        from pages import dashboard
        dashboard.show()

elif page == "🎯 Goals":
    st.title("🎯 Financial Goals")
    from pages import goals
    goals.show()

elif page == "💾 Save Progress":
    st.title("💾 Save Your Progress")
    
    if st.session_state.mode == 'logged_in':
        st.success("✅ Your data is automatically saved!")
    else:
        st.info("💡 Create an account to save your financial progress and access it from anywhere.")
        
        from pages import auth
        auth.show_save_prompt()
