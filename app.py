import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="GrowWiser 💸 - Personal Financial Mentor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================
st.session_state.setdefault("page", "login")
st.session_state.setdefault("view", "overview")

# =========================================================
# GLOBAL STYLING (Animated, Professional)
# =========================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(255,255,255,0.90), rgba(255,255,255,0.90)),
        url("https://images.unsplash.com/photo-1554224154-22dec7ec8818");
    background-size: cover;
    background-position: center;
    animation: bgmove 35s ease-in-out infinite alternate;
}

@keyframes bgmove {
    from {background-position: center top;}
    to {background-position: center bottom;}
}

h1, h2, h3, p, label {
    color: #0f172a !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FINANCIAL LOGIC FUNCTIONS
# =========================================================
def savings_rate(savings, income):
    return (savings / income) * 100 if income > 0 else 0

def sip_future_value(P, annual_rate, years=10):
    r = annual_rate / 12
    n = years * 12
    return P * ((1 + r)**n - 1) / r

# =========================================================
# EMAIL VALIDATION FUNCTION
# =========================================================
allowed_domains = ["gmail.com", "outlook.com", "yahoo.com", "company.com"]

def is_valid_email(email):
    if " " in email:
        return False, "Email cannot contain spaces"
    if "@" not in email or "." not in email:
        return False, "Invalid email format"
    #domain = email.split("@")[-1]
   # Split local part and domain
    local_part, domain = email.split("@", 1)

    # Local part must be alphanumeric
    if not local_part.isalnum():
        return False, "Invalid email name: only letters and numbers allowed before '@'"


    if domain not in allowed_domains:
        return False, f"Only {', '.join(allowed_domains)} allowed"
    return True, "Valid mail address"

# =========================================================
# LOGIN (MOCK – DEMO SAFE)
# =========================================================
if st.session_state.page == "login":

    st.title("GrowWiser 💸")
    st.subheader("A Personal Financial Mentor")

    st.markdown("### Log-in")

    name = st.text_input("Name")
    email = st.text_input("Email")

    # Live feedback
    if email:
        valid, msg = is_valid_email(email)
        if not valid:
            st.warning(msg)

    if st.button("Enter Dashboard"):
        if not name:
            st.warning("Please enter your name.")
        else:
            valid, msg = is_valid_email(email)
            if not valid:
                st.error(msg)
            else:
                st.session_state.page = "dashboard"
                st.rerun()

    

# =========================================================
# DASHBOARD


# =========================================================

#FEATURE 1: Smart transaction intelligence + categorization
else:

    st.title("Financial Intelligence Dashboard")

    # ---------------- INPUT STRIP ----------------
    c1, c2, c3, c4, c5, c6 , c7= st.columns(7)

    income = c1.number_input("Monthly Income (₹)", min_value=0, step=1000)
    rent = c2.number_input("Rent (₹)", min_value=0, step=500)
    food = c3.number_input("Food / Delivery (₹)", min_value=0, step=500)
    transport = c4.number_input("Transport (₹)", min_value=0, step=500)
    lifestyle = c5.number_input("Lifestyle (₹)", min_value=0, step=500)
    sip = c6.number_input("SIP (₹)", min_value=0, step=500)
    mutual_funds = c6.number_input("Mutual Funds (₹)", min_value=0, step=500)
    credit_card_emi = c6.number_input("Credit Card EMI (₹)", min_value=0, step=500)
    months_invested = c6.number_input("Months Invested", min_value=0, step=1)
    annual_rate = c7.number_input("Annual Rate of Return (%)", min_value=0.0, step=0.1)
    annual_rate = annual_rate / 100  # Convert percentage to decimal
    
    # ---------------- CORE CALCULATIONS ----------------
    needs = rent + transport
    wants = food + lifestyle
    investments = sip + mutual_funds
    debt = credit_card_emi

    total_expense = needs + wants + investments + debt
    savings = income - total_expense
    
    debt_ratio = (debt / income) * 100 if income > 0 else 0
    needs_ratio = (needs / income)*100 if income > 0 else 0
    s_rate = savings_rate(savings, income)*100 if income > 0 else 0
    wants_ratio = (wants / income) *100 if income > 0 else 0
    investment_ratio = (investments / income)*100 if income > 0 else 0


# =========================================================
#FEATURE 2: HEALTH SCORE 
# =========================================================

    # ---------------- HEALTH SCORE ----------------
    score = 100
    if debt ==0 and savings== 0 and needs == 0 and wants == 0 and investments== 0:
        debt_ratio = 0
        needs_ratio =0
        s_rate =0
        wants_ratio =0
        investment_ratio =0
        score=0
    
    
    else:
        if s_rate < 20:
            score -= 20
        if wants_ratio > 0.30:
            score -= 15
        if investment_ratio < 0.10:
            score -= 20
        if debt_ratio > 30:
            score -= 30
            ##score = max(score, 0)
    
    investment_consistency = min(months_invested / 12, 1)
    score += int(investment_consistency * 15)
    score = min(score, 100)

# =========================================================


# =========================================================

    # ---------------- NAV ----------------
    n1, n2, n3, n4, n5, n6 = st.columns(6)
    if n1.button("📊 Overview"):
        st.session_state.view = "overview"
    if n2.button("🔮 Future Impact Mapping"):
        st.session_state.view = "Future Impact Mapping"
    if n3.button("🧠 Mentor Mode"):
        st.session_state.view = "Mentor Mode"
    if n4.button("💰 Tax Estimation"):
        st.session_state.view = "💰 Tax Estimation"
    if n5.button("🎯 Goal Based Empire Plan"):
        st.session_state.view = "Goal Based Empire Plan"
    if n6.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    # =====================================================
    # OVERVIEW
    # =====================================================
    if st.session_state.view == "overview":

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Income", f"₹{income}")
        k2.metric("Expenses", f"₹{total_expense}")
        k3.metric("Savings", f"₹{savings}")
        k4.metric("Health Score", f"{score}/100")

        df = pd.DataFrame({
            "Category": ["Needs", "Wants", "Investments", "Savings", "Debt"],
            "Amount": [needs, wants, investments, savings, debt]
        })

        c1, c2 = st.columns(2)

        with c1:
            pie = px.pie(df, names="Category", values="Amount", hole=0.55)
            pie.update_layout(height=300)
            st.plotly_chart(pie, use_container_width=True)

        with c2:
            bar = px.bar(df, x="Category", y="Amount")
            bar.update_layout(height=300)
            st.plotly_chart(bar, use_container_width=True)


    # =====================================================
    #FEATURE 3: HABIT - FUTURE IMPACT PLANNING
    # =====================================================
    elif st.session_state.view == "Future Impact Mapping":

        st.subheader("🔮 Future Consequences")

        if food > 0:
            loss = sip_future_value(food, annual_rate)
            st.warning(
                f"🍔 Food delivery of ₹{food}/month → "
                f"₹{loss:,.0f} lost in 10 years if invested instead."
            )

        if lifestyle > 0:
            loss = sip_future_value(lifestyle, annual_rate)
            st.warning(
                f"🎮 Lifestyle spending of ₹{lifestyle}/month → "
                f"₹{loss:,.0f} opportunity loss in 10 years."
            )

        if investments == 0:
            st.error(
                "📉 No investments detected.\n\n"
                "Continuing this habit means no compounding growth."
            )
        else:
            gain = sip_future_value(investments, annual_rate)
            st.success(
                f"📈 Investing ₹{investments}/month → "
                f"₹{gain:,.0f} in 10 years at {annual_rate*100:.1f}% p.a."
            )

        st.success(
            "Small monthly habits compound into massive future outcomes."
        ) 
        
    # =====================================================
    #Feature 4: ESTIMATE TAX
    # =====================================================
    elif st.session_state.view == "💰 Tax Estimation":
        st.subheader("💰 Tax Estimation")
        annual_income = income * 12
        tax = 0
        st.markdown("### 🧾 Income Tax Estimator (Budget 2025 – New Regime)"
        )

        if annual_income >= 400000:
            slabs = [
                (400000, 0.00),
            (800000, 0.05),
            (1200000, 0.10),
            (1600000, 0.15),
            (2000000, 0.20),
            (2400000, 0.25),
            (float("inf"), 0.30),
            ]

            tax = 0
            previous_limit = 0

            for limit, rate in slabs:
                if annual_income > previous_limit:
                    taxable_amount = min(annual_income, limit) - previous_limit
                    tax += taxable_amount * rate
                    previous_limit = limit
                else:
                     break

            st.info(f"Estimated Income Tax: ₹{tax:,.0f}")

            eff_rate = (tax / annual_income) * 100
            st.caption(f"Effective Tax Rate: {eff_rate:.2f}%")
        else:
            st.info("Please enter a valid annual income to estimate tax.")


    # =====================================================
    #Feature 5: HEALTHY GOAL BASED EMPIRE PLAN
    # =====================================================
    elif st.session_state.view == "Goal Based Empire Plan":
        st.subheader("🎯 Goal Based Empire Plan")
        st.markdown(
            """
            1. **Emergency Fund**: Save at least 6 months of expenses in a liquid fund.
            2. **Debt Management**: Prioritise paying off high-interest debt first.
            3. **Investment Strategy**: Allocate at least 15% of income to diversified investments.
            4. **Retirement Planning**: Start a retirement fund and contribute regularly.
            5. **Regular Reviews**: Review financial goals and progress every 6 months.
            """
        )
        
    # =====================================================
    #Feature 6: INSIGHTS + RECOMMENDATIONS + MENTOR MODE
    # =====================================================
    elif st.session_state.view == "Mentor Mode":

        st.subheader("🧠 Financial Risk & Guidance")

        if wants_ratio > 0.30:
            st.error("High discretionary spending detected (>30%).")

        if investment_ratio < 0.10:
            st.warning("Low investment ratio. Wealth growth is weak.")

        if s_rate < 20:
            st.warning("Savings rate below healthy threshold.")

        st.markdown("### 🎯 Personalised Recommendations")

        recommendations = []

        if investment_ratio < 0.10:
            recommendations.append("Start a ₹2,000 SIP in an index fund.")
        if wants_ratio > 0.30:
            recommendations.append("Reduce food delivery & lifestyle spending.")
        if s_rate < 20:
            recommendations.append("Target saving at least 20% of income.")
        if debt_ratio > 0.50:
            recommendations.append("HIGH RISK!\nFocus on reducing high-interest debt.\nAvoid new debt.")
        for r in recommendations:
            st.info(r)

        st.markdown("### 🧑‍🏫 Mentor Message")

        if investment_ratio < 0.10:
            mentor = "Your money is idle instead of compounding."
        elif wants_ratio > 0.30:
            mentor = "Lifestyle inflation is delaying your future goals."
        elif s_rate < 20:
            mentor = "You need stronger financial discipline."
        else:
            mentor = "You are making disciplined financial decisions."

        st.success(mentor)