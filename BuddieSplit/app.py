import streamlit as st
import requests
from decimal import Decimal, ROUND_HALF_UP

# --- CONFIG & STYLING ---
st.set_page_config(page_title="BuddySplit INR", page_icon="🇮🇳", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div.stButton > button:first-child {
        background-color: #008080; color: white; border-radius: 10px;
    }
    .main-card {
        padding: 20px; border-radius: 15px; background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def get_exchange_rate(target_currency):
    """Fetches real-time rate for 1 INR to Target."""
    try:
        # Using a free API for 2026 real-time rates
        url = f"https://api.exchangerate-api.com/v4/latest/INR"
        response = requests.get(url).json()
        return response['rates'].get(target_currency, 1.0)
    except:
        return 0.012  # Fallback estimate (1 INR to USD)

def calculate_split(amount, people, tip_pct):
    amount = Decimal(str(amount))
    tip = (amount * (Decimal(str(tip_pct)) / 100)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    total = amount + tip
    
    base_share = (total / people).quantize(Decimal('0.01'), ROUND_HALF_UP)
    shares = [base_share] * people
    
    # Adjust for the penny gap
    remainder = total - (base_share * people)
    shares[0] += remainder
    
    return float(total), [float(s) for s in shares]

# --- UI ---
st.title("🇮🇳 BuddySplit")
st.write("Split bills with friends in Rupees & Foreign Currency.")

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        bill_amount = st.number_input("Bill Amount (₹)", min_value=0.0, step=1.0, format="%.2f")
    with col2:
        num_buddies = st.number_input("Number of Buddies", min_value=1, step=1, value=2)

    tip_percent = st.select_slider("Add a Tip (%)", options=[0, 5, 10, 12, 15, 20], value=0)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOREIGN CURRENCY OPTION ---
st.write("---")
use_foreign = st.checkbox("🌍 Add Foreign Currency Option")

target_curr = "USD"
rate = 1.0

if use_foreign:
    target_curr = st.selectbox("Select Foreign Currency", ["USD", "EUR", "GBP", "AED", "SGD"])
    rate = get_exchange_rate(target_curr)
    st.caption(f"Live Rate: 1 ₹ ≈ {rate:.4f} {target_curr}")

# --- CALCULATION & DISPLAY ---
if bill_amount > 0:
    # 1. Calculate in INR
    total_inr, shares_inr = calculate_split(bill_amount, num_buddies, tip_percent)
    
    st.subheader("📊 The Split")
    
    # Visual Breakdown
    c1, c2 = st.columns(2)
    c1.metric("Total Bill (with tip)", f"₹{total_inr:,.2f}")
    if use_foreign:
        total_foreign = total_inr * rate
        c2.metric(f"Total in {target_curr}", f"{total_foreign:,.2f}")

    st.write("### 👥 Buddy Breakdown")
    for i, share in enumerate(shares_inr):
        name = f"Buddy {i+1}"
        if i == 0: name += " (Payer 💳)"
        
        # Displaying both currencies side-by-side
        if use_foreign:
            foreign_share = share * rate
            st.info(f"**{name}**: ₹{share:,.2f}  |  **{foreign_share:,.2f} {target_curr}**")
        else:
            st.info(f"**{name}**: ₹{share:,.2f}")

else:
    st.info("Enter a bill amount to see the magic happen!")